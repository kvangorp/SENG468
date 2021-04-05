import React, { Component } from "react";
import {commandLogger, errorLogger} from '../transactionLogger.js'
import axios from "axios";
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
  ListGroup,
  ListGroupItem,
  Collapse,
  Card,
  CardBody
} from "reactstrap";

// This creates a class for the modal created by clicking the Display Summary Button
export default class DisplaySummaryModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
        userId: '',
        balance: '',
        pending: '',
        stocks: '',
        triggers: '',
        transactions: '',
        stocksButton: false,
        triggersButton: false,
        transactionsButton: false
    };
  }

  // When user input is sent or buttons are clicked, this method updates modal state
  handleChange = (e) => {
    let { name, value } = e.target;
    const state = { ...this.state, [name]: value };
    this.setState(state);
  };

  triggerDisplaySummary = () => {
    this.handleDisplaySummary()
  }

  // Sends user input as a command to the Display Summary 
  // endpoint, and logs transaction in database 
  handleDisplaySummary = () => {
    let userId = this.state.userId;

    var request = {
      'userId': userId,
      'transactionNum':1,
    }
    axios.post('http://localhost:8080/api/commands/display_summary/', request)
    .then((response) => {
      console.log(response);
      this.handleResponse(response);
      commandLogger(userId,0.0,"DISPLAY_SUMMARY");
    })
    .catch((error) => {
      errorLogger(userId,"DISPLAY_SUMMARY");
    }) 
  }

  handleResponse = (response) => {
    this.setState({
      balance: response.data.balance,
      pending: response.data.pending,
      stocks: response.data.stocks,
      triggers: response.data.triggers,
      transactions: response.data.transactions
    })
  }

  // When a user clicks this button, a box 
  // opens showing the stocks the use has
  toggleStocksButton = () => {
    this.setState({stocksButton: !this.state.stocksButton})
  }

  // When a user clicks this button, a box 
  // opens showing the triggers the use has set
  toggleTriggersButton = () => {
    this.setState({triggersButton: !this.state.triggersButton})
  }

  // When a user clicks this button, a box 
  // opens showing the transactions the use has made
  toggleTransactionsButton = () => {
    this.setState({transactionsButton: !this.state.transactionsButton})
  }

  // Creates and associates buttons for the modal users to interact with
  render() {
    const { toggle } = this.props;

    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}>Display Summary</ModalHeader>
        <ModalBody>
          <Form>
          <FormGroup>
              <Label for="userId">User ID</Label>
              <Input
                type="text"
                id="userId"
                name="userId"
                value={this.state.userId}
                onChange={this.handleChange}
                placeholder="Enter User ID"
              />
            </FormGroup>
          </Form>
          <ListGroup>
            <ListGroupItem>UserID: {this.state.userId}</ListGroupItem>
            <ListGroupItem>Balance: {this.state.balance}</ListGroupItem>
            <ListGroupItem>Pending: {this.state.pending}</ListGroupItem>
            <Button color="primary" onClick={this.toggleStocksButton} style={{ marginBottom: '1rem' }}>Stocks</Button>
            <Collapse isOpen={this.state.stocksButton}>
              <Card>
                <CardBody>{JSON.stringify(this.state.stocks)}</CardBody>
              </Card>
            </Collapse>
            <Button color="primary" onClick={this.toggleTriggersButton} style={{ marginBottom: '1rem' }}>Triggers</Button>
            <Collapse isOpen={this.state.triggersButton}>
              <Card>
                <CardBody>{JSON.stringify(this.state.triggers)}</CardBody>
              </Card>
            </Collapse>
            <Button color="primary" onClick={this.toggleTransactionsButton} style={{ marginBottom: '1rem' }}>Transactions</Button>
            <Collapse isOpen={this.state.transactionsButton}>
              <Card>
                <CardBody>{JSON.stringify(this.state.transactions)}</CardBody>
              </Card>
            </Collapse>
          </ListGroup>
        </ModalBody>
        <ModalFooter>
          <Button
            color="success"
            onClick={this.triggerDisplaySummary}
          >
            Display Summary
          </Button>
        </ModalFooter>
      </Modal>
    );
  }
}