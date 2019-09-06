import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import I18n from "i18n-js";
import "./Registration.scss";
import Button from "../components/Button";

export default function Registration({props}) {

    const renderStepDivider = step =>
        (<div key={step} className="step-divider">
            {[1, 2, 3].map(i => <span key={i}><FontAwesomeIcon icon="circle"/></span>)}
        </div>);

    const renderStep = step => {
        return (<div key={step} className="step">
            <div>
                <span className="step-title">{I18n.t(`registration.${step}`)}</span>
            </div>
            <FontAwesomeIcon icon={I18n.t(`registration.${step}Icon`)}
                             className="step-icon"/>
        </div>);
    };
    const renderStepPart = step => step.startsWith(".") ? renderStepDivider(step) : renderStep(step);
    return (
        <div className="mod-registration">
            <div className="intro">
                <p>{I18n.t("registration.title")}</p>
            </div>
            <div className="step-container">
                {["agreeToService", ".1.", "verify", ".2.", "validate"].map(i => renderStepPart(i))}
            </div>
            <div className="intro">
                <p>{I18n.t("registration.registration")}</p>
                <ul className="steps">
                    <li>{I18n.t("registration.agreeToServiceStep")}</li>
                    <li>{I18n.t("registration.verifyStep")}</li>
                    <li>{I18n.t("registration.validateStep")}</li>
                </ul>
                <Button onClick={() => props.history.push("/aup")}
                        txt={I18n.t("registration.continueToService")}/>
            </div>
        </div>
    )
};
