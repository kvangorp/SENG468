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
import BuyModal from './BuyModal.js'

// This creates a class for the modal created by clicking the Buy Button
export default class CommitModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeItem: this.props.activeItem,
      commitModal: false,
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
            // This button triggers a commit Buy event, 
            // which sends a string "commit" to BuyModal.js, 
            // triggering the commit buy
            onClick={() => onSave('commit')}//this.commitBuy(this.state.activeItem)}
          >
              Commit Buy
          </Button>
          <Button
            color='danger'
            // This button triggers a cancel Buy event, 
            // which sends a string "cancel" to BuyModal.js, 
            // triggering the cancel buy
            onClick={() => onSave('cancel')}//this.cancelBuy(this.state.activeItem)}
          >
              Cancel Buy
          </Button>
        </ModalFooter>
      </Modal>
    );
  }
    
}