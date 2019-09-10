import React from "react";
import {completeRegistration, openEmailVerifications, regenerateEmail, verifyEmail} from "../api";
import I18n from "i18n-js";
import "./Validation.scss";
import Button from "../components/Button";
import {isEmpty} from "../utils/Utils";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";


class Validation extends React.Component {

  constructor(props, context) {
    super(props, context);
    this.state = {
      emailVerifications: [],
    };
  }

  componentDidMount = () => {
    openEmailVerifications().then(res => {
      const {user} = this.props;
      const remoteVerifications = user.remote_accounts.map(ra => ra.attributes.mail)
        .flat()
        .filter(mail => !isEmpty(mail))
        .map(mail => ({email: mail, verified: true, remote: true, code: ""}));

      const userVerifications = res.map(verification => ({
        email: verification.email,
        verified: verification.verified,
        remote: false,
        code: ""
      }));
      const emailVerifications = [...userVerifications, ...remoteVerifications];
      this.setState({emailVerifications: emailVerifications});
    });
  };


  isValid = () => {
    const {emailVerifications} = this.state;
    const anyNoneVerified = emailVerifications.some(ev => !ev.verified);
    return !anyNoneVerified;
  };


  submit = () => {
    if (this.isValid()) {
      completeRegistration().then(() => this.props.history.push("/finish"));
    }
  };

  changeCode = index => e => {
    const {emailVerifications} = this.state;
    emailVerifications[index].code = e.target.value;
    this.setState({emailVerifications: [...emailVerifications]});
  };

  verify = index => () => {
    const {emailVerifications} = this.state;
    const emailVerification = emailVerifications[index];
    verifyEmail(emailVerification.code, emailVerification.email)
      .then(res => {
        emailVerifications[index].verified = true;
        emailVerifications[index].error = false;
        this.setState({emailVerifications: [...emailVerifications]});
      }).catch(e => {
      emailVerifications[index].error = true;
      this.setState({emailVerifications: [...emailVerifications]});
    });
  };

  regenerate = index => () => {
    const {emailVerifications} = this.state;
    const emailVerification = emailVerifications[index];
    regenerateEmail(emailVerification.email)
      .then(res => this.componentDidMount());
  };

  renderEmailVerification = (verification, index) => {
    const iconName = verification.verified ? "envelope" : "envelope-open";
    const txt = verification.verified ? (verification.remote ? "verifiedByProvider" : "verifiedByCode") : "enterCode";
    const className = isEmpty(verification.code) ? "disabled" : "";
    return (
      <div key={index}>
        <div className="verification">
          <FontAwesomeIcon icon={iconName}/>
          <input type="text" disabled={true} value={verification.email}/>
          <span className="verification-status">{I18n.t(`validations.${txt}`)}</span>
          {!verification.verified &&
          <input type="text" className="code" onChange={this.changeCode(index)} value={verification.code}/>}
          {!verification.verified && <Button className={`green ${className}`} txt={I18n.t("validations.verify")}
                                             onClick={this.verify(index)}/>}
        </div>
        {verification.error && <div>
          <span className="error">{I18n.t("validations.validationError")}</span>
          <Button className="orange regenerate" txt={I18n.t("validations.regenerate")}
                  onClick={this.regenerate(index)}/>
        </div>}
      </div>);
  };

  render() {
    const {emailVerifications, initial} = this.state;
    const disabledSubmit = !initial && !this.isValid();
    return (
      <div className="mod-validations">
        <div className="intro">
          <p dangerouslySetInnerHTML={{__html: I18n.t("validations.title")}}/>
        </div>
        <div className="validations-form">
          {
            emailVerifications.map((verification, index) => this.renderEmailVerification(verification, index))
          }
        </div>
        <div className="intro">
          <p dangerouslySetInnerHTML={{__html: I18n.t("validations.confirmation")}}/>
        </div>

        <section className="actions">
          <Button disabled={disabledSubmit} txt={I18n.t("validations.update")}
                  onClick={this.submit}/>
        </section>


      </div>);
  }
  ;
}

export default Validation;