import React from 'react';
import {
    AppRegistry,
} from 'react-native';

import CEOEmailScreen from './pages/RNCEOEmailScreen';

userInfo = () => {
    var userInfo = this.props["userInfo"];
}

class iOSRN extends React.Component {
    render() {

        return (
            <CEOEmailScreen screenProps={this.props["userInfo"]}/>
        )
    }
}

AppRegistry.registerComponent('iOSRN', () => iOSRN);