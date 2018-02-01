import React, { Component } from 'react';
import ReactList from 'react-list';

import './myList.css'

const filesHeader = {
    index:'行数',
    name:'名称',
    version:'版本',
    'MD5':'MD5值',
    time:'更新时间',
    fileUrl:'下载地址',
}

export default class MyList extends Component {
  static defaultProps = {
    filesDatas: [filesHeader],
    patchDatas: [filesHeader],
  }

  _renderItem(type,index, key) {
    let item = type === 'files' ? this.props.filesDatas[index] : this.props.patchDatas[index]
    let lastColumn = index === 0 ? (<label className='cellColumn'> {item.fileUrl} </label>) :
    (<a className='cellColumn' href={item.fileUrl}>点击下载 </a>);

    return(
      <div key={key} className='listItem'>
        <label className='cellColumn'> {item.index || index} </label>
        <label className='cellColumn'> {item.name} </label>
        <label className='cellColumn'> {item.version} </label>
        <label className='cellColumn'> {item.MD5} </label>
        <label className='cellColumn'> {item.time} </label>
        {lastColumn}
      </div>
    )
  }

  render() {
    return (
      <div>
        <h1>Files</h1>
        <div style={{overflow: 'auto', maxHeight: 1000}}>
          <ReactList
            itemRenderer={this._renderItem.bind(this, 'files')}
            length={this.props.filesDatas.length}
            type='uniform'
          />
        </div>
        <h1>Patchs</h1>
        <div style={{overflow: 'auto', maxHeight: 1000}}>
          <ReactList
            itemRenderer={this._renderItem.bind(this, 'patchs')}
            length={this.props.patchDatas.length}
            type='uniform'
          />
        </div>
      </div>
    );
  }


}
