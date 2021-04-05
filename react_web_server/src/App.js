import logo from './logo.svg';
import './App.css';
import React, { Component } from "react";
import BuyModal from "./components/BuyModal";
import SellModal from "./components/SellModal";
import AddModal from "./components/AddModal";
import QuoteModal from "./components/QuoteModal";
import SetBuyAmountModal from "./components/SetBuyAmountModal";
import SetBuyTriggerModal from "./components/SetBuyTriggerModal";
import CancelSetBuyModal from "./components/CancelSetBuyModal";
import SetSellAmountModal from "./components/SetSellAmountModal";
import SetSellTriggerModal from "./components/SetSellTriggerModal";
import CancelSetSellModal from "./components/CancelSetSellModal";
import DisplaySummaryModal from "./components/DisplaySummaryModal";
import DumplogModal from "./components/DumplogModal";
import axios from "axios";

//TransactioNum count

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      buyModal: false,
      sellModal:false,
      addModal:false,
      quoteModal:false,
      setBuyAmountModal: false,
      setBuyTriggerModal: false,
      cancelSetBuyModal: false,
      setSellAmountModal: false,
      setSellTriggerModal: false,
      cancelSetSellModal: false,
      displaySummaryModal: false,
      dumplogModal: false
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
//******************************************************************************************************* */  
  renderSellButton = () => {
    return (
      <div className="commandButton">
        <ul>
          <button 
            className="commandButton"
            onClick={() => this.sellStocks()}
          >Sell</button>
        </ul>
        {this.state.sellModal ? (
          <SellModal
            activeItem={this.state.activeItem}
            toggle={this.toggle}
            onSave={this.handleSellSubmit}
          />
        ) : null}
      </div> 
    );
  }
  sellToggle = () => {
    this.setState({ sellModal: !this.state.sellModal });
  };
  
  handleSellSubmit = (item) => {
    this.sellToggle();
    var request={
      "stockSymbol":item["stockSymbol"],
      'userId': item["userId"],
      'amount': parseFloat(item["amount"])
    }
    axios.post('http://localhost:8080/api/commands/sell/', request,)
    .then((response) => {
      console.log(response);
      this.commandLogger(item["userId"],parseFloat(item["amount"]),"SELL",item["stockSymbol"]);
      alert("save " + JSON.stringify(request)); 
    })
    .catch((error) => {
      if(error.status!==500){
        this.errorLogger(item["userId"],"SELL")
      }
    })
    
  };
  sellStocks = () => {
    const item = {userid:"",quotesymbol: "", buyamount: ""}
    this.setState({activeItem: item, sellModal: !this.state.sellModal})
  }
//******************************************************************************************************* */  
  renderBuyButton = () => {
    return (
      <div className="commandButton">
        <ul>
          <button 
            className="commandButton"
            onClick={() => this.buyStocks()}
          >Buy</button>
        </ul>
        {this.state.buyModal ? (
          <BuyModal
            activeItem={this.state.activeItem}
            toggle={this.toggle}
            onSave={this.handleBuySubmit}
          />
        ) : null}
      </div> 
      
    );
  }
  buyStocks = () => {
    const item = {userid:"",quotesymbol: "", buyamount: ""}
    this.setState({activeItem: item, buyModal: !this.state.buyModal})
  }
  
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
      alert("save " + JSON.stringify(request)); 
    })
    .catch((error) => {
      this.errorLogger(item["userId"],"BUY")
    })

   
  };
  buyToggle = () => {
    this.setState({ buyModal: !this.state.buyModal });
  };

  
//******************************************************************************************************** */
  renderAddButton = () => {
    return (
      <div className="commandButton">
        <ul>
          <button 
            className="commandButton"
            onClick={() => this.addStocks()}
          >Add</button>
        </ul>
        {this.state.addModal ? (
          <AddModal
            activeItem={this.state.activeItem}
            toggle={this.toggle}
            onSave={this.handleAddSubmit}
          />
        ) : null}
      </div> 
      
    );
  }
  addStocks = () => {
    const item = {userid:"",amount: ""}
    this.setState({activeItem: item, addModal: !this.state.addModal})
  }

  handleAddSubmit = (item) => {
    this.addToggle();
    var request={
      'userId': item["userId"],
      'amount': parseFloat(item["amount"]),
      'transactionNum':1
    }
    axios.post('http://localhost:8080/api/commands/add/', request)
    .then((response) => {
      console.log(response);
      this.commandLogger(item["userId"],parseFloat(item["amount"]),"ADD");
    })
    .catch((error) => {
      this.errorLogger(item["userId"],parseFloat(item["amount"]),"ADD")
    })    
  };
  addToggle = () => {
    this.setState({ addModal: !this.state.addModal });
  };
//******************************************************************************************************** */
  renderQuoteButton = () => {
    return (
      <div className="commandButton">
        <ul>
          <button 
            className="commandButton"
            onClick={() => this.quoteStocks()}
          >Quote</button>
        </ul>
        {this.state.quoteModal ? (
          <QuoteModal
            activeItem={this.state.activeItem}
            toggle={this.toggle}
            onSave={this.handleQuoteSubmit}
          />
        ) : null}
      </div> 
      
    );
  }
  quoteStocks = () => {
    const item = {userid:"",stockSymbol: ""}
    this.setState({activeItem: item, quoteModal: !this.state.quoteModal})
  }

  handleQuoteSubmit = (item) => {
    this.quoteToggle();
    var request={
      "stockSymbol":item["stockSymbol"],
      'userId': item["userId"],
      'transactionNum': 1,
    }
    axios.post('http://localhost:8080/api/commands/quote/', request)
    .then((response) => {
      console.log(response);
      this.commandLogger(item["userId"],parseFloat(item["amount"]),"QUOTE");
      alert("Quote" + JSON.stringify(response.data)); 
    })
    .catch((error) => {
      this.errorLogger(item["userId"],"QUOTE")
    })    
    
  };
  quoteToggle = () => {
    this.setState({ quoteModal: !this.state.quoteModal });
  };

  // ********************************************************************************************************/
  renderSetBuyAmountButton = () => {
    return (
      <div className="commandButton">
        <ul>
          <button 
            className="commandButton"
            onClick={this.toggleSetBuyAmountModal}
          >Set Buy Amount</button>
        </ul>
        {this.state.setBuyAmountModal ? (
          <SetBuyAmountModal
            toggle={this.toggleSetBuyAmountModal}
          />
        ) : null}
      </div> 
      
    );
  }

  toggleSetBuyAmountModal = () => {
    this.setState({setBuyAmountModal: !this.state.setBuyAmountModal})
  }

  // ********************************************************************************************************/
  renderSetBuyTriggerButton = () => {
    return (
      <div className="commandButton">
        <ul>
          <button 
            className="commandButton"
            onClick={this.toggleSetBuyTriggerModal}
          >Set Buy Trigger</button>
        </ul>
        {this.state.setBuyTriggerModal ? (
          <SetBuyTriggerModal
            toggle={this.toggleSetBuyTriggerModal}
          />
        ) : null}
      </div> 
      
    );
  }

  toggleSetBuyTriggerModal = () => {
    this.setState({setBuyTriggerModal: !this.state.setBuyTriggerModal})
  }

  // ********************************************************************************************************/
  renderCancelSetBuyButton = () => {
    return (
      <div className="commandButton">
        <ul>
          <button 
            className="commandButton"
            onClick={this.toggleCancelSetBuyModal}
          >Cancel Set Buy</button>
        </ul>
        {this.state.cancelSetBuyModal ? (
          <CancelSetBuyModal
            toggle={this.toggleCancelSetBuyModal}
          />
        ) : null}
      </div> 
      
    );
  }

  toggleCancelSetBuyModal = () => {
    this.setState({cancelSetBuyModal: !this.state.cancelSetBuyModal})
  }

  // ********************************************************************************************************/
  renderSetSellAmountButton = () => {
    return (
      <div className="commandButton">
        <ul>
          <button 
            className="commandButton"
            onClick={this.toggleSetSellAmountModal}
          >Set Sell Amount</button>
        </ul>
        {this.state.setSellAmountModal ? (
          <SetSellAmountModal
            toggle={this.toggleSetSellAmountModal}
          />
        ) : null}
      </div> 
      
    );
  }

  toggleSetSellAmountModal = () => {
    this.setState({setSellAmountModal: !this.state.setSellAmountModal})
  }

  // ********************************************************************************************************/
  renderSetSellTriggerButton = () => {
    return (
      <div className="commandButton">
        <ul>
          <button 
            className="commandButton"
            onClick={this.toggleSetSellTriggerModal}
          >Set Sell Trigger</button>
        </ul>
        {this.state.setSellTriggerModal ? (
          <SetSellTriggerModal
            toggle={this.toggleSetSellTriggerModal}
          />
        ) : null}
      </div> 
      
    );
  }

  toggleSetSellTriggerModal = () => {
    this.setState({setSellTriggerModal: !this.state.setSellTriggerModal})
  }

  // ********************************************************************************************************/
  renderCancelSetSellButton = () => {
    return (
      <div className="commandButton">
        <ul>
          <button 
            className="commandButton"
            onClick={this.toggleCancelSetSellModal}
          >Cancel Set Sell</button>
        </ul>
        {this.state.cancelSetSellModal ? (
          <CancelSetSellModal
            toggle={this.toggleCancelSetSellModal}
          />
        ) : null}
      </div> 
      
    );
  }

  toggleCancelSetSellModal = () => {
    this.setState({cancelSetSellModal: !this.state.cancelSetSellModal})
  }

  // ********************************************************************************************************/
  renderDisplaySummaryButton = () => {
    return (
      <div className="commandButton">
        <ul>
          <button 
            className="commandButton"
            onClick={this.toggleDisplaySummaryModal}
          >Display Summary</button>
        </ul>
        {this.state.displaySummaryModal ? (
          <DisplaySummaryModal
            toggle={this.toggleDisplaySummaryModal}
          />
        ) : null}
      </div> 
      
    );
  }

  toggleDisplaySummaryModal = () => {
    this.setState({displaySummaryModal: !this.state.displaySummaryModal})
  }

  // ********************************************************************************************************/
  renderDumplogButton = () => {
    return (
      <div className="commandButton">
        <ul>
          <button 
            className="commandButton"
            onClick={this.toggleDumplogModal}
          >Dumplog</button>
        </ul>
        {this.state.dumplogModal ? (
          <DumplogModal
            toggle={this.toggleDumplogModal}
          />
        ) : null}
      </div> 
      
    );
  }

  toggleDumplogModal = () => {
    this.setState({dumplogModal: !this.state.dumplogModal})
  }
 
  render() {
    return (
      <main className="container">
        <h1 className="text-white text-uppercase text-center my-4">Todo app</h1>
        <div className="row">
          <div className="col-md-6 col-sm-10 mx-auto p-0">
            <div className="card p-3">
              <div className="mb-4">
                <p>
                  Day Trading Commands
                </p>
              </div>
              {this.renderAddButton()}
              {this.renderQuoteButton()}
              {this.renderBuyButton()}
              {this.renderSellButton()}
              {this.renderSetBuyAmountButton()}
              {this.renderSetBuyTriggerButton()}
              {this.renderCancelSetBuyButton()}
              {this.renderSetSellAmountButton()}
              {this.renderSetSellTriggerButton()}
              {this.renderCancelSetSellButton()}
              {this.renderDisplaySummaryButton()}
              {this.renderDumplogButton()}
            </div>
          </div>
        </div>
      </main>
      
    );
  }
}

export default App;
