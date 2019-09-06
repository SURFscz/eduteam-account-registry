import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import I18n from "i18n-js";
import "./Aup.scss";
import Button from "../components/Button";

export default function Aup({user, ...props}) {

    return (
        <div className="mod-aup">

            <div className="intro">
                <p>{JSON.stringify(user)}</p>
            </div>

            <Button onClick={() => props.history.push("/aup")}
                    txt={I18n.t("registration.continueToService")}/>
        </div>
    )
};
