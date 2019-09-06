import React from "react";
import I18n from "i18n-js";
import {Link} from "react-router-dom";
import logo from "../images/eduteams_logo.jpg";
import "./Header.scss";

export const Header = () => (
    <div className={`header-container`}>
        <div className="header">
            <Link to="/"><img className="logo" src={logo} alt=""/></Link>
            <div className="header-top">
                <p className="title first">{I18n.t("header.title")}</p>
                <a className="help" href={I18n.t("header.links.helpUrl")} rel="noopener noreferrer"
                   target="_blank">{I18n.t("header.links.help")}</a>
            </div>
        </div>
    </div>
);

