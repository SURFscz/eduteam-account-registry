import React from "react";
import I18n from "i18n-js";

import MDSpinner from "react-md-spinner";
import spinner from "../utils/Spin.js";

import {Link} from "react-router-dom";

import "./Navigation.scss";

export default class Navigation extends React.PureComponent {

    constructor() {
        super();
        this.state = {
            loading: false,
        };
    }

    componentDidMount() {
        spinner.onStart = () => this.setState({loading: true});
        spinner.onStop = () => this.setState({loading: false});
    }

    renderItem(href, value, className = "menu-item") {
        return (
            <Link className={`${className} active` } to={href}>{I18n.t("navigation." + value)}</Link>
        );
    }

    renderSpinner = () =>
        this.state.loading ? <div className="spinner">
            <MDSpinner size={42}
                       singleColor={"#FFD700"}
                       duration={1000}
                       borderSize={8}/>
        </div> : null;

    render() {
        const {currentUser} = this.props;
        return (
            <div className="navigation-container">
                <div className="navigation">
                    {!currentUser.is_complete && this.renderItem("/registration", "registration")}
                    {currentUser.is_complete && this.renderItem("/account", "account")}
                </div>
                {this.renderSpinner()}
            </div>
        );
    }
}
