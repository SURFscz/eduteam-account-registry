import React, {useEffect, useState} from "react";
import I18n from "i18n-js";
import "./Aup.scss";
import Button from "../components/Button";
import {agreeAup, aupLinks} from "../api";
import CheckBox from "../components/CheckBox";


export default function Aup({user, ...props}) {
    const [aup, setAup] = useState({pdf_link: undefined, pdf: "", html: ""});
    const [agreed, setAgreed] = useState(false);

    useEffect(() => {
        aupLinks().then(res => setAup(res))
    }, []);

    return (
        <div className="mod-aup">

            <div className="intro">
                {<p dangerouslySetInnerHTML={{__html: I18n.t("aup.title1")}}/>}
                {<p dangerouslySetInnerHTML={{__html: I18n.t("aup.title2")}}/>}
                {<p dangerouslySetInnerHTML={{__html: I18n.t("aup.title3")}}/>}
            </div>

            <div className="htmlAup" dangerouslySetInnerHTML={{__html: aup.html}}/>

            <div className="download">
                <CheckBox name="aup" value={agreed} info={I18n.t("aup.agreeWithTerms")}
                          onChange={e => setAgreed(e.target.checked)}/>
                <a href={aup.pdf_link} className="pdf" download={aup.pdf} target="_blank" rel="noopener noreferrer">
                    {I18n.t("aup.downloadPdf")}
                </a>
            </div>


            <Button className="proceed" onClick={() => agreeAup().then(() => props.history.push("/attributes"))}
                    txt={I18n.t("aup.continueToValidation")} disabled={!agreed}/>
        </div>
    )
};
