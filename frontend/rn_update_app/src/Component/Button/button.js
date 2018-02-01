import React, { Component } from 'react';
import './button.css';

export default class Button extends Component {

    constructor(props) {
        super(props);
        this.state = {
            res: "",
        }
    }

    post() {
        console.log("click post button")
        const react_this = this;
        var url="http://127.0.0.1:8080/index/rest_api/ymm/"
        let content = {'mychoice' : '1'}
        fetch(url, {
          method: 'post',
          headers: {"Content-Type" : "application/x-www-form-urlencoded"},
          body:'mychoice=1',
        }).then(response => response.text())
          .then(responseText => {
            console.log('post response is:', responseText);
            react_this.setState({
              res:responseText
            })
          })
        .catch((responseData) => {
          console.log(responseData)
        })
    }

    get(){
        var url="http://127.0.0.1:8080/index/rest_api/ymm/"
        console.log("click get button")
        const react_this = this;
        fetch(url)
        .then(response => response.text())
        .then(responseText => {
            console.log('post response is:', responseText);
            react_this.setState({
              res:responseText
            })
          })
        .catch((responseData) => {
          console.log(responseData)
        })
    }
    render() {
      var res = this.state.res
      return (
        <div>
          <button className='btn' onClick={this.get.bind(this)}> GET </button>
          <button className='btn' onClick={this.post.bind(this)}> POST </button>
          <p> result:  { res }</p>
        </div>
      );
    }
}
