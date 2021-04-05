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
import CommitSellModal from './CommitCancelSellModal.js'
import axios from "axios";


export default class SellModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeItem: this.props.activeItem,
      sellModal: false,
      commitSellModal:false,
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

  handleChange = (e) => {
    let { name, value } = e.target;

    if (e.target.type === "checkbox") {
      value = e.target.checked;
    }

    const activeItem = { ...this.state.activeItem, [name]: value };

    this.setState({ activeItem });
  };

  handleSellSubmit = (item) => {
    var request={
      'transactionNum': 1,
      "stockSymbol":item["stockSymbol"],
      'userId': item["userId"],
      'amount': parseFloat(item["amount"])
    }
    axios.post('http://localhost:8080/api/commands/sell/', request,)
    .then((response) => {
      console.log(response);
      this.commandLogger(item["userId"],parseFloat(item["amount"]),"SELL",item["stockSymbol"]);
      //alert("save " + JSON.stringify(request)); 
      this.setState({commitSellModal: !this.state.commitSellModal}, () => {setTimeout(this.handleClose, 55000)})
    })
    .catch((error) => {
      if(error.response.status!==412){
        this.commandLogger(item["userId"],parseFloat(item["amount"]),"SELL")
        this.errorLogger(item["userId"],parseFloat(item["amount"]),"SELL")
      }else{ 
        this.commandLogger(item["userId"],parseFloat(item["amount"]),"SELL")
        alert("You don't own this stock, or you don't have enough of it to sell at this price.");
        setTimeout(window.location.reload(),1000)
      }
    })
    
  };

  handleClose = () =>{
    this.setState({commitSellModal: !this.state.commitSellModal})
    var request={
      'userId': this.state.activeItem["userId"],
      'transactionNum':1,
    }
    axios.post('http://localhost:8080/api/commands/cancel_sell/', request)
    .then((response) => {
      console.log(response);
      this.commandLogger(this.state.activeItem["userId"],0.0, "CANCEL_SELL"); 
      setTimeout(window.location.reload(),2000)
    }) 
    
  }

  triggerCommitSellModal = () => {
    this.handleSellSubmit(this.state.activeItem)
  }
  closeCommitModal = ()  => {
    this.setState({commitSellModal: !this.state.commitSellModal})
    setTimeout(window.location.reload(),1000)
  }
  commitSell = (item) => {
    var request={
      'userId': item["userId"],
      'transactionNum':1,
    }
    axios.post('http://localhost:8080/api/commands/commit_sell/', request)
    .then((response) => {
      console.log(response);
      this.commandLogger(item["userId"],item["amount"],"COMMIT_SELL")
      this.closeCommitModal()
      setTimeout(window.location.reload(),1000)
      alert("Sell Transaction Committed Successfully"); 

    })
    .catch((error) => {
      this.errorLogger(item["userId"],item["amount"],"COMMIT_SELL")
      this.closeCommitModal()
      setTimeout(window.location.reload(),1000)
    }) 
  }
  cancelSell = (item) => {
    var request={
        'userId': item["userId"],
        'transactionNum':1,
      }
      axios.post('http://localhost:8080/api/commands/cancel_sell/', request)
      .then((response) => {
        console.log(response);
        this.commandLogger(item["userId"],item["amount"],"CANCEL_SELL");
        this.closeCommitModal()
        setTimeout(window.location.reload(),1000)
        alert("Sell Transaction Cancelled Successfully"); 

      })
      .catch((error) => {
        this.errorLogger(item["userId"],item["amount"],"CANCEL_SELL")
        this.closeCommitModal()
        setTimeout(window.location.reload(),1000)
      })   
      
  } 
  commitOrCancel = (string) => {
    if(string==='commit'){
      this.commitSell(this.state.activeItem)
    }else{
      this.cancelSell(this.state.activeItem)
    }
  }
  
  render() {
    const { toggle, onSave } = this.props;

    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}>Sell Stock</ModalHeader>
        <ModalBody>
          <Form>
            <FormGroup sell="true">
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
            <FormGroup sell="true">
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
            <FormGroup sell="true">
              <Label for="">Amount</Label>
              <Input
                type="number"
                id="sell_amount"
                name="amount"
                value={this.state.activeItem.title}
                onChange={this.handleChange}
                placeholder="Enter Dollar amount of stock to sell"
              />
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button
            color="success"
            onClick={() => this.triggerCommitSellModal()}
          >
            Sell
          </Button>
          {this.state.commitSellModal ? (
          <CommitSellModal
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