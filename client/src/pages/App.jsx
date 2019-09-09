import React from "react";
import "./App.scss";
import {Header} from "../components/Header";
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import NotFound from "../pages/NotFound";
import ServerError from "../pages/ServerError";
import Navigation from "../components/Navigation";
import {config, me, reportError} from "../api";
import "../locale/en";
import ErrorDialog from "../components/ErrorDialog";
import Registration from "./Registration";
import Footer from "../components/Footer";
import {addIcons} from "../utils/IconLibrary";
import {pseudoGuid} from "../utils/Utils";
import Redirect from "react-router-dom/Redirect";
import Aup from "./Aup";
import Attributes from "./Attributes";

addIcons();

class App extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.state = {
            loading: true,
            currentUser: {},
            config: {},
            error: false,
            errorDialogOpen: false,
            errorDialogAction: () => this.setState({errorDialogOpen: false})
        };
        window.onerror = (msg, url, line, col, err) => {
            if (err && err.response && err.response.status === 404) {
                this.props.history.push("/404");
                return;
            }
            this.setState({errorDialogOpen: true});
            const info = err || {};
            const response = info.response || {};
            const error = {
                userAgent: navigator.userAgent,
                message: msg,
                url: url,
                line: line,
                col: col,
                error: info.message,
                stack: info.stack,
                targetUrl: response.url,
                status: response.status
            };
            reportError(error);
        };
    }

    handleBackendDown = () => {
        const location = window.location;
        const alreadyRetried = location.href.indexOf("guid") > -1;
        if (alreadyRetried) {
            window.location.href = `${location.protocol}//${location.hostname}${location.port ? ":" + location.port : ""}/error`;
        } else {
            //302 redirects from Shib are cached by the browser. We force a one-time reload
            const guid = pseudoGuid();
            window.location.href = `${location.href}?guid=${guid}`;
        }
    };

    componentDidMount() {
        const location = window.location;
        if (location.href.indexOf("error") > -1) {
            this.setState({loading: false});
        } else {
            config().then(res => {
                this.setState({config: res}, () => {
                    me().then(currentUser => {
                        this.setState({currentUser: currentUser, loading: false});
                    }).catch(() => {
                        window.location.href = res.login_url
                    })
                });
            }).catch(() => this.handleBackendDown());
        }
    }

    refreshUser = () => me().then(json => this.setState({currentUser: json}));

    render() {
        const {
            loading, errorDialogAction, errorDialogOpen, currentUser
        } = this.state;
        if (loading) {
            return null; // render null when app is not ready yet
        }
        return (
            <Router>
                <div className="app-container">
                    {currentUser && <div>
                        <Header currentUser={currentUser}/>
                        <Navigation currentUser={currentUser}/>
                        <ErrorDialog isOpen={errorDialogOpen}
                                     close={errorDialogAction}/>
                    </div>}
                    <Switch>
                        <Route exact path="/" render={() => {
                            return currentUser.is_complete ? <Redirect to="/registration"/> :
                                <Redirect to="/registration"/>
                        }}/>
                        <Route path="/registration"
                               render={props => <Registration props={props}/>}/>

                        <Route path="/aup"
                               render={props => <Aup user={currentUser} {...props}/>}/>

                        <Route exact path="/attributes"
                               render={props => <Attributes user={currentUser}
                                                              {...props}/>}/>

                        <Route exact path="/validate"
                               render={props => <Registration user={currentUser}
                                                              {...props}/>}/>

                        <Route exact path="/finish"
                               render={props => <Registration user={currentUser}
                                                              {...props}/>}/>

                        <Route path="/error" render={props => <ServerError {...props}/>}/>

                        <Route render={props => <NotFound currentUser={currentUser} {...props}/>}/>
                    </Switch>
                    <Footer/>
                </div>
            </Router>

        );
    }
}

export default App;
