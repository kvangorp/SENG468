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

// This creates a class for the modal created by clicking the Quote Button
export default class QuoteModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeItem: this.props.activeItem,
      quoteModal: false,
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
  
  // Creates and associates input fields for the modal users to interact with
  render() {
    const { toggle, onSave } = this.props;

    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}>Get a Stock Quote</ModalHeader>
        <ModalBody>
          <Form>
          <FormGroup quote="true">
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
            <FormGroup quote="true">
              <Label for="stock_symbol">Stock Symbol</Label>
              <Input
                type="text"
                id="stock_symbol"
                name="stockSymbol"
                value={this.state.activeItem.title}
                onChange={this.handleChange}
                placeholder="Enter Quote Symbol"
              />
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button
            color="success"
            // When this Quote button is clicked the user 
            // input is saved in a JSON object and returned 
            // to the web server as the body of a HTTP packet
            onClick={() => onSave(this.state.activeItem)}
          >
            Get Quote
          </Button>
        </ModalFooter>
      </Modal>
    );
  }
    
}