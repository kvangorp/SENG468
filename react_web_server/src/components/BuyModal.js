import CommitModal from './CommitCancelBuyModal.js'
import React, { Component } from "react";
import {
  Button,
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Form,
  FormGroup,
  Input,
  Label,
} from "reactstrap";
import commandLogger from '../App.js'
import axios from "axios";

// This creates a class for the modal created by clicking the Buy Button
export default class BuyModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeItem: this.props.activeItem,
      buyModal: false,
      commitModal:false,
    };
  }

  

  commandLogger = (userid='', amount=0.0, command='', stockSymbol='', transactionNum=1) => {
    var request = {
        'type': 'userCommand',
        'timestamp': (new Date()).getTime(),
        'server': 'WS',
        'transactionNum': transactionNum,
        'command': command,
        'username': userid,
        'stockSymbol': stockSymbol,
        'funds': amount
    }
    axios.post('http://localhost:8080/api/transactions/', request)
    .then((response) => {
      console.log(response);
    }) 
  }

  errorLogger = (userid='', command='', transactionNum=1) => {
    var request = {
        "type": "errorEvent",
        "timestamp": (new Date()).getTime(),
        "server": 'WS',
        "transactionNum": transactionNum,
        "command": command,
        "username": userid,
        "errorMessage": "Error while processing command."
    }
    axios.post('http://localhost:8080/api/transactions/', request)
    .then((response) => {
      console.log(response);
    }) 
  }

  // When user input is sent or buttons are clicked, this method updates modal state
  handleChange = (e) => {
    let { name, value } = e.target;

    if (e.target.type === "checkbox") {
      value = e.target.checked;
    }

    // Populate item based on user input
    const activeItem = { ...this.state.activeItem, [name]: value };

    this.setState({ activeItem });
  };
  
  // Logs initial buy transaction, then opens 
  // secondary modal to allow user to commit 
  // or cancel their buy command
  handleBuySubmit = (item) => {
    var request={
      'transactionNum': 1,
      "stockSymbol":item["stockSymbol"],
      'userId': item["userId"],
      'amount': parseFloat(item["amount"])
    }
    axios.post('http://localhost:8080/api/commands/buy/', request)
    .then((response) => {
      console.log(response);
      this.commandLogger(item["userId"],parseFloat(item["amount"]),"BUY",item["stockSymbol"]);
      // Initiates modal for a 60 second lifespan
      this.setState({commitModal: !this.state.commitModal}, () => {setTimeout(this.handleClose, 55000)})
    })
    .catch((error) => {
      if(error.response.status!==412){
        this.commandLogger(item["userId"],parseFloat(item["amount"]),"BUY")
        this.errorLogger(item["userId"],parseFloat(item["amount"]),"BUY")
      }else{ 
        this.commandLogger(item["userId"],parseFloat(item["amount"]),"BUY")
        alert("You don't have enough money in your account to buy this stock");
        setTimeout(window.location.reload(),1000)
      }
    })
  }

  handleClose = () =>{
    this.setState({commitModal: !this.state.commitModal})
    var request={
      'userId': this.state.activeItem["userId"],
      'transactionNum':1,
    }
    axios.post('http://localhost:8080/api/commands/cancel_buy/', request)
    .then((response) => {
      console.log(response);
      this.commandLogger(this.state.activeItem["userId"],0.0, "CANCEL_BUY");
      setTimeout(window.location.reload(),2000)
    }) 
  }

  triggerCommitModal = () => {
    this.handleBuySubmit(this.state.activeItem)
  }

  closeCommitModal = ()  => {
    this.setState({commitModal: !this.state.commitModal})
    setTimeout(window.location.reload(),1000) 
  }

  // If user clicks button to commit buy 
  // command, a commit buy is logged, and 
  // the server returns to home page
  commitBuy = (item) => {
    var request={
      'userId': item["userId"],
      'transactionNum':1,
    }
    axios.post('http://localhost:8080/api/commands/commit_buy/', request)
    .then((response) => {
      console.log(response);
      this.commandLogger(item["userId"],item["amount"],"COMMIT_BUY")
      this.closeCommitModal()
      setTimeout(window.location.reload(),1000)
      alert("Buy Transaction Committed Successfully"); 
    })
    .catch((error) => {
      this.errorLogger(item["userId"],item["amount"],"COMMIT_BUY")
      this.closeCommitModal()
      setTimeout(window.location.reload(),1000)
    }) 
  }

  // If user clicks button to cancel buy 
  // command, a cancel buy is logged, and 
  // the server returns to home page
  cancelBuy = (item) => {
    var request={
        'userId': item["userId"],
        'transactionNum':1,
      }
      axios.post('http://localhost:8080/api/commands/cancel_buy/', request)
      .then((response) => {
        console.log(response);
        this.commandLogger(item["userId"],item["amount"],"CANCEL_BUY");
        this.closeCommitModal()
        setTimeout(window.location.reload(),1000)
        alert("Buy Transaction Cancelled Successfully"); 
      })
      .catch((error) => {
        this.errorLogger(item["userId"],item["amount"],"CANCEL_BUY")
        this.closeCommitModal()
        setTimeout(window.location.reload(),1000)
      })   
      
  }
  
  commitOrCancel = (string) => {
    if(string==='commit'){
      this.commitBuy(this.state.activeItem)
    }else{
      this.cancelBuy(this.state.activeItem)
    }
  }

  // Creates and associates input fields for the modal users to interact with
  render() {
    const { toggle, onSave } = this.props;

    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}>Buy Stock</ModalHeader>
        <ModalBody>
          <Form>
          <FormGroup buy="true">
              <Label for="stock_symbol">User ID</Label>
              <Input
                type="text"
                id="user_id"
                name="userId"
                value={this.state.activeItem.title}
                onChange={this.handleChange}
                placeholder="Enter User ID"
              />
            </FormGroup>
            <FormGroup buy="true">
              <Label for="stock_symbol">Quote Symbol</Label>
              <Input
                type="text"
                id="stock_symbol"
                name="stockSymbol"
                value={this.state.activeItem.title}
                onChange={this.handleChange}
                placeholder="Enter Quote Symbol"
              />
            </FormGroup>
            <FormGroup buy="true">
              <Label for="">Amount</Label>
              <Input
                type="number"
                id="buy_amount"
                name="amount"
                value={this.state.activeItem.title}
                onChange={this.handleChange}
                placeholder="Enter Dollar amount of stock"
              />
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button
            color="success"
            onClick={() =>{
              this.triggerCommitModal()
              }
            }
          >
            Buy
          </Button>
          {this.state.commitModal ? (
          <CommitModal
            activeItem={this.state.activeItem}
            toggle={this.toggle}
            onSave={this.commitOrCancel}
          />
        ) : null}
        </ModalFooter>
      </Modal>
    );
  }
}