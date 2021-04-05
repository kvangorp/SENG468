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

export default class AddModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeItem: this.props.activeItem,
      addModal: false,
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
        <ModalHeader toggle={toggle}>Add Money to Account</ModalHeader>
        <ModalBody>
          <Form>
          <FormGroup add="true">
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
            <FormGroup add="true">
              <Label for="">Amount</Label>
              <Input
                type="number"
                id="buy_amount"
                name="amount"
                value={this.state.activeItem.title}
                onChange={this.handleChange}
                placeholder="Enter Dollar amount to add to account"
              />
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button
            color="success"
            onClick={() => onSave(this.state.activeItem)}
          >
            Add
          </Button>
        </ModalFooter>
      </Modal>
    );
  }
    
}