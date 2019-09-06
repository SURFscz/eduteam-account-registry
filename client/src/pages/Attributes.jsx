import React from "react";
import {updateUser} from "../api";
import I18n from "i18n-js";
import InputField from "../components/InputField";
import "./Attributes.scss";
import Button from "../components/Button";
import {isEmpty} from "../utils/Utils";
import SelectField from "../components/SelectField";
import {validEmailRegExp} from "../validations/regExps";
import CheckBox from "../components/CheckBox";

class Attributes extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.state = {
            names: [""],
            emails: [""],
            phones: [""],
            required: ["name", "short_name"],
            address: "",
            country: "",
            refLanguage: ""
        };
    }

    validateEmail = e => {
        const email = e.target.value;
        const {invalidInputs} = this.state;
        const inValid = !isEmpty(email) && !validEmailRegExp.test(email);
        this.setState({invalidInputs: {...invalidInputs, email: inValid}});
    };

    submit = () => {
        const {initial} = this.state;
        if (initial) {
            this.setState({initial: false}, this.doSubmit)
        } else {
            this.doSubmit();
        }
    };

    isValid = () => {
        const {invalidInputs} = this.state;
        const inValid = Object.keys(invalidInputs).some(key => invalidInputs[key]);
        return !inValid;
    };


    doSubmit = () => {
        if (this.isValid()) {
            updateUser(this.state).then(() => this.props.history.push("/validate"));
        }
    };

    render() {
        const {
            names, emails, phones, address, country, refLanguage, initial
        } = this.state;
        const disabledSubmit = !initial && !this.isValid();
        return (
            <div className="mod-attributes">
                <div className="intro">
                    <p>{<p dangerouslySetInnerHTML={{__html: I18n.t("attributes.title")}}/>}</p>
                </div>
                <div className="attributes-form">
                    <InputField value={service.name}
                                name={I18n.t("userServiceProfile.service__name")}
                                disabled={true}
                                link={`/services/${service.id}`}
                                history={this.props.history}/>

                    <InputField value={authorisation_group.name}
                                name={I18n.t("userServiceProfile.authorisation_group__name")}
                                disabled={true}
                                link={authorisation_group ? `/collaboration-authorisation-group-details/${authorisation_group.collaboration.id}/${authorisation_group.id}` : null}
                                history={this.props.history}/>

                    <InputField value={authorisation_group.collaboration.name}
                                name={I18n.t("userServiceProfile.authorisation_group__collaboration__name")}
                                disabled={true}
                                link={`/collaborations/${authorisation_group.collaboration.id}`}
                                history={this.props.history}/>

                    <InputField value={name}
                                name={I18n.t("userServiceProfile.name")}
                                placeholder={I18n.t("userServiceProfile.namePlaceholder")}
                                onChange={e => this.setState({name: e.target.value})}/>

                    <InputField value={email}
                                name={I18n.t("userServiceProfile.email")}
                                placeholder={I18n.t("userServiceProfile.emailPlaceholder")}
                                onChange={e => this.setState({
                                    email: e.target.value,
                                    invalidInputs: !isEmpty(e.target.value) ? invalidInputs : {
                                        ...invalidInputs,
                                        email: false
                                    }
                                })}
                                onBlur={this.validateEmail}/>
                    {invalidInputs["email"] && <span
                        className="error">{I18n.t("forms.invalidInput", {name: "email"})}</span>}
                    <InputField value={address}
                                name={I18n.t("userServiceProfile.address")}
                                placeholder={I18n.t("userServiceProfile.addressPlaceholder")}
                                onChange={e => this.setState({address: e.target.value})}/>

                    <InputField value={identifier}
                                name={I18n.t("userServiceProfile.identifier")}
                                placeholder={I18n.t("userServiceProfile.identifierPlaceholder")}
                                onChange={e => this.setState({identifier: e.target.value})}
                                toolTip={I18n.t("userServiceProfile.identifierTooltip")}
                                disabled={true}/>

                    <InputField value={ssh_key}
                                name={I18n.t("userServiceProfile.ssh_key")}
                                placeholder={I18n.t("userServiceProfile.ssh_keyPlaceholder")}
                                onChange={e => this.setState({ssh_key: e.target.value})}
                                toolTip={I18n.t("userServiceProfile.ssh_keyTooltip")}
                                onBlur={this.validateSSHKey}
                                fileUpload={true}
                                fileName={fileName}
                                fileInputKey={fileInputKey}
                                onFileRemoval={this.onFileRemoval}
                                onFileUpload={this.onFileUpload}
                                acceptFileFormat=".pub"/>
                    {fileTypeError &&
                    <span
                        className="error">{I18n.t("userServiceProfile.sshKeyError")}</span>}
                    {showConvertSSHKey &&
                    <CheckBox name="convertSSHKey" value={convertSSHKey}
                              info={I18n.t("userServiceProfile.sshConvertInfo")}
                              onChange={e => this.setState({convertSSHKey: e.target.checked})}/>}

                    <SelectField value={this.statusOptions.find(option => status === option.value)}
                                 options={this.statusOptions}
                                 name={I18n.t("userServiceProfile.status")}
                                 clearable={false}
                                 placeholder={I18n.t("userServiceProfile.statusPlaceholder")}
                                 onChange={selectedOption => this.setState({status: selectedOption ? selectedOption.value : null})}
                    />
                    <InputField value={role}
                                name={I18n.t("userServiceProfile.role")}
                                disabled={true}/>

                    <section className="actions">
                        <Button disabled={disabledSubmit} txt={I18n.t("attributes.update")}
                                onClick={this.submit}/>
                    </section>

                </div>
            </div>);
    }
    ;
}

export default Attributes;