import React, { Component } from 'react';
import './App.css';
import YMMUpload from './Component/Upload/uploadfile.js'
import FilesList from './Component/List/myList.js'
import { SERVER_CONF } from './Component/YMMConst';

const filesHeader = {
    index:'行数',
    name:'名称',
    version:'版本',
    'MD5':'MD5值',
    time:'更新时间',
    fileUrl:'下载地址',
}

class App extends Component {

  constructor(props) {
    super(props)
    this.state = {
      filesDatas:[],
      patchDatas:[]
    }
  }

  componentWillMount() {
    this._getFilesData();
  }

  _getFilesData() {
    let react_this = this;
    var url= SERVER_CONF.base_url + SERVER_CONF.update_path + 'managefiles/'
    fetch(url)
    .then(response => response.text())
    .then(responseText => {
        console.log('post response is:', JSON.parse(responseText));
        let filesData = JSON.parse(responseText);
        let files = filesData['files']
        let patchs = filesData['patchs']
        files.unshift(filesHeader)
        patchs.unshift(filesHeader)
        react_this.setState({
          filesDatas:files,
          patchDatas:patchs
        })
      })
    .catch((responseData) => {
      console.log(responseData)
    })
  }

  _uploadSuccess() {
    this._getFilesData();
  }

  _patchesSuccess() {
    this._getFilesData();
  }

  render() {
    return (
      <div className="App">
        <YMMUpload uploadSuccess= {this._uploadSuccess.bind(this)} patchesSuccess = {this._patchesSuccess.bind(this)}/>
        <FilesList filesDatas={this.state.filesDatas} patchDatas={this.state.patchDatas}/>
      </div>
    );
  }
}



export default App;
