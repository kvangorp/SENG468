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

export default class CustomModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeItem: this.props.activeItem,
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
        <ModalHeader toggle={toggle}>Buy Stock</ModalHeader>
        <ModalBody>
          <Form>
            <FormGroup buy>
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
            <FormGroup buy>
              <Label for="">Amount</Label>
              <Input
                type="text"
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
            onClick={() => onSave(this.state.activeItem)}
          >
            Buy
          </Button>
        </ModalFooter>
      </Modal>
    );
  }
    
}