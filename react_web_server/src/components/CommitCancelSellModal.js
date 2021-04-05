import commandLogger from '../App.js'
import errorLogger from '../App.js'
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
import App from "../App";
import axios from "axios";
import SellModal from './SellModal.js'

// This creates a class for the modal created by clicking the Sell Button
export default class CommitSellModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeItem: this.props.activeItem,
      commitSellModal: false,
    };
    
  }

  // When user input is sent or buttons are clicked, this method updates modal state
  handleChange = (e) => {
    let { name, value } = e.target;

    if (e.target.type === "checkbox") {
      value = e.target.checked;
    }

    const activeItem = { ...this.state.activeItem, [name]: value };

    this.setState({ activeItem });
  };
  
  // Creates and associates buttons for the modal users to interact with
  render() {
    const { toggle, onSave } = this.props;

    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalFooter>
          <p>What would you do to do? </p>
          <Button
            color="success"
            // This button triggers a commit Sell event, 
            // which sends a string "commit" to SellModal.js, 
            // triggering the commit Sell
            onClick={() => onSave('commit')}//this.commitBuy(this.state.activeItem)}
          >
              Commit Sell
          </Button>
          <Button
            color='danger'
            // This button triggers a cancel Sell event, 
            // which sends a string "cancel" to SellModal.js, 
            // triggering the cancel Sell
            onClick={() => onSave('cancel')}//this.cancelBuy(this.state.activeItem)}
          >
              Cancel Sell
          </Button>
        </ModalFooter>
      </Modal>
    );
  }
    
}