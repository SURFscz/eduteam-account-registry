import React from "react";
import I18n from "i18n-js";
import {Link, NavLink} from "react-router-dom";
import logo from "../images/eduteams_logo.jpg";
import "./Header.scss";
import {isEmpty, pseudoGuid, stopEvent} from "../utils/Utils";
import LanguageSelector from "./LanguageSelector";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import UserProfile from "./UserProfile";
import ReactTooltip from "react-tooltip";
import {getParameterByName} from "../utils/QueryParameters";
import Button from "./Button";
import {provision} from "../api";

export default class Header extends React.PureComponent {

    constructor() {
        super();
        this.state = {
            dropDownActive: false
        };
    }

    renderProfileLink(currentUser) {
        return (
            <a href="/profile" className="welcome-link" onClick={this.handleToggle}>
                {currentUser.name}
                {this.renderDropDownIndicator()}
            </a>
        );
    }

    handleToggle = e => {
        stopEvent(e);
        this.setState({dropDownActive: !this.state.dropDownActive});
    };

    renderDropDownIndicator = () => this.state.dropDownActive ? <FontAwesomeIcon icon="caret-up"/> :
        <FontAwesomeIcon icon="caret-down"/>;


    renderDropDown = currentUser => this.state.dropDownActive ? <UserProfile currentUser={currentUser}/> : null;

    render() {
        const {currentUser} = this.props;
        return (
            <div className={`header-container`}>
                <div className="header">
                    <Link to="/"><img className="logo" src={logo} alt=""/></Link>

                    <p className="title first">{I18n.t("header.title")}</p>
                    <ul className="links">
                        <li className="user-profile border-left">
                            {this.renderProfileLink(currentUser)}
                            {this.renderDropDown(currentUser)}
                        </li>
                        <li className="help border-left">
                            <a href={I18n.t("header.links.helpUrl")} rel="noopener noreferrer"
                               target="_blank">{I18n.t("header.links.help")}</a>
                        </li>
                    </ul>
                </div>
            </div>
        );
    }
}
