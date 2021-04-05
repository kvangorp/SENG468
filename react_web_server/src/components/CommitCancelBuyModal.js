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

 
export default class CommitModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeItem: this.props.activeItem,
      commitModal: false,
    };
    
  }
  handleChange = (e) => {
    let { name, value } = e.target;

    if (e.target.type === "checkbox") {
      value = e.target.checked;
    }

    const activeItem = { ...this.state.activeItem, [name]: value };

    this.setState({ activeItem });
  };
  
  render() {
    const { toggle, onSave } = this.props;

    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalFooter>
          <p>What would you do to do? </p>
          <Button
            color="success"
            onClick={() => onSave('commit')}//this.commitBuy(this.state.activeItem)}
          >
              Commit Buy
          </Button>
          <Button
            color='danger'
            onClick={() => onSave('cancel')}//this.cancelBuy(this.state.activeItem)}
          >
              Cancel Buy
          </Button>
        </ModalFooter>
      </Modal>
    );
  }
    
}