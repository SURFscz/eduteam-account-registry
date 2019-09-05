import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import I18n from "i18n-js";
import "./Registration.scss";

const Registration = ({}) => {
    const renderStepDivider = step =>
        (<div key={step} className="step-divider">
            {[1, 2, 3].map(i => <span key={i}><FontAwesomeIcon icon="circle"/></span>)}
        </div>);
    const renderStep = step => {
        return (<div key={step} className="step active">
            <span className="step-info" data-for={step} data-tip>
            </span>
            <div>
                <span className="step-number">{step}</span>
                <span className="step-title">{I18n.t(`registration.step${step}.title`)}</span>
            </div>
            <span className="step-sub">{I18n.t(`registration.step${step}.sub`)}</span>
            <FontAwesomeIcon icon={I18n.t(`registration.step${step}.icon`)}
                             className="step-icon"/>
        </div>);
    };
    const renderStepPart = step => step.startsWith(".") ? renderStepDivider(step.substring(1, 3)) : renderStep(step);
    return <div className="mod-registration">
        <div className="step-container">
            {["1", ".1.", "2", ".2.", "3"].map(i => renderStepPart(i))}
        </div>

    </div>
};

export default Registration;