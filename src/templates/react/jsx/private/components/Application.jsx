import React from 'react';
// http://minutemailer.github.io/react-popup/
import Popup from 'react-popup';
import moment from 'moment';

import api from '../../utils/api';
import Loader from '../../components/Loader.jsx';
import Router from '../../components/Router.jsx';


class Application extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            isLoader : false,
            route : this.routeByHash()
        };
        this.setRouteByHash = this.setRouteByHash.bind(this);
        this.loaderOpen = this.loaderOpen.bind(this);
        this.loaderClose = this.loaderClose.bind(this);
        api.setLoader(this.loaderOpen, this.loaderClose);
        moment.locale('ru');
    }

    componentWillMount() {
        window.addEventListener('hashchange', this.setRouteByHash, false);
    }

    componentWillUnmount() {
        window.removeEventListener('hashchange', this.setRouteByHash);
    }

    render() {
        const props = {
            route : this.state.route
        };
        return <div className="app-wrapper">
            {this.state.isLoader ? <Loader /> : null}
            <Router route={this.state.route} css="private-layout" />
            <Popup />
        </div>;
    }

    routeByHash() {
        return location.hash.substr(3).split('/');
    }

    setRouteByHash() {
        this.setState({route : this.routeByHash()});
    }

    loaderOpen() {
        this.setState({
            isLoader : true
        });
    }

    loaderClose() {
        this.setState({
            isLoader : false
        });
    }

}

export default Application;
