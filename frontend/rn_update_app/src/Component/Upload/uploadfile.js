import Upload from 'rc-upload'
import React, { Component } from 'react';
import './uploadFile.css'
import { SERVER_CONF } from '../YMMConst'

export default class YMMUpload extends Component {
  constructor(props) {
    super(props)
    this.state = {
      res: '',
      version: '',
    }
    let that = this;

    this.uploaderProps = {
      action: SERVER_CONF.base_url + SERVER_CONF.update_path + 'upload/',
      multiple: true,
      beforeUpload(file) {
        console.log('beforeUpload', file.name);
      },
      onStart: (file) => {
        console.log('onStart', file.name);
        that.setState({
          res: file.name + ' start upload'
        })
      },
      onSuccess(file) {
        console.log('onSuccess', file);
        that.setState({
          res: file
        })
        that.props.uploadSuccess();
      },
      onProgress(step, file) {
        console.log('onProgress', Math.round(step.percent), file.name);
      },
      onError(err) {
        console.log('onError', err);
      },
  };

  }

  _getPatch() {
    var url= SERVER_CONF.base_url + SERVER_CONF.update_path + 'upload/?MD5=aeaaf408686284aa9f35cf347b8ef663&version=1.1'
    const react_this = this;
    fetch(url)
    .then(response => response.text())
    .then(responseText => {
        console.log('post response is:', responseText);
        react_this.setState({
          res:responseText
        })
        react_this.props.patchesSuccess();
      })
    .catch((responseData) => {
      console.log(responseData)
    })
  }

  _versionValueChanged(event) {
    this.setState({
      version:event.target.value,
      data:{version: event.target.value}
    })
  }

  render() {
    var res = this.state.res
    return (
      <div className='content'>
        <h4> 上传新文件 aaaa</h4>
        <label>
           version:
           <input type="text" value={this.state.version} onChange={(event)=>this._versionValueChanged(event)} />
        </label>
         <Upload className='upload' {...this.uploaderProps} data={ {version: this.state.version}} ref="inner"><a>开始上传</a></Upload>
         <br/>
         <button className='btn' onClick={() => this._getPatch()}>获取patch信息</button>
        <p> result:  { res }</p>
      </div>
    );
  }

}
