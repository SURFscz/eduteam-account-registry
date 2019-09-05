import "@babel/polyfill";
import {polyfill} from "es6-promise";
import "isomorphic-fetch";
import React from 'react';
import ReactDOM from 'react-dom';
import './stylesheets/index.scss';
import App from './pages/App';
import moment from "moment-timezone";
import I18n from "i18n-js";
import "./locale/en";


polyfill();

I18n.locale = "en";
moment.locale(I18n.locale);
ReactDOM.render(<App/>, document.getElementById("app"));