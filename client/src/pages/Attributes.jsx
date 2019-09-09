import React from "react";
import {updateUser} from "../api";
import I18n from "i18n-js";
import InputField from "../components/InputField";
import "./Attributes.scss";
import Button from "../components/Button";
import {isEmpty} from "../utils/Utils";
import SelectField from "../components/SelectField";
import {validEmailRegExp} from "../validations/regExps";
import {languages} from "../data/languages";
import {countries} from "../data/countries";

class Attributes extends React.Component {

  constructor(props, context) {
    super(props, context);
    this.state = {
      names: [""],
      emails: [""],
      phones: [""],
      address: "",
      country: "",
      refLanguage: "",
      initial: true,
      invalidInputs: {}

    };
    this.required = ["names", "emails"];
    this.countryOptions = countries.map(country => ({value: country, label: country}));
    this.languageOptions = languages.map(language => ({value: language, label: language}));
    this.excludedAttributes = ["eduPersonTargetedID", "eduPersonAffiliation", "schacHomeOrganization", "eduPersonPrincipalName"]
  }

  validateEmail = index => e => {
    const email = e.target.value;
    const {invalidInputs} = this.state;
    const inValid = !isEmpty(email) && !validEmailRegExp.test(email);
    this.setState({invalidInputs: {...invalidInputs, [`email${index}`]: inValid}});
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
    const requiredMissing = this.required.some(name => {
      const attr = this.state[name];
      return Array.isArray(attr) ? isEmpty(attr.filter(val => !isEmpty(val))) : isEmpty(attr);
    });
    return !inValid && !requiredMissing;
  };


  doSubmit = () => {
    if (this.isValid()) {
      updateUser(this.state).then(() => this.props.history.push("/validate"));
    }
  };

  changeAttr = (name, index = null) => e => {
    let attrs = this.state[name];
    if (Array.isArray(attrs)) {
      attrs[index] = e.target.value;
    } else {
      attrs = e.target.value;
    }
    this.setState({[name]: attrs})
  };

  addAttr = name => () => {
    const attrs = this.state[name];
    attrs.push("");
    this.setState({[name]: attrs})
  };

  deleteAttr = (name, index) => () => {
    const attrs = this.state[name];
    attrs.splice(index, 1);
    this.setState({[name]: attrs})

  };

  render() {
    const {
      names, emails, phones, address, country, refLanguage, initial, invalidInputs
    } = this.state;
    const {user} = this.props;
    const attributes = {};
    user.remote_accounts.forEach(remoteAccount => {
      Object.keys(remoteAccount.attributes).forEach(attrName => {
        let translation = I18n.t(`attributes.${attrName}`);
        translation = translation.indexOf("missing") > -1 ? attrName : translation;
        if (!this.excludedAttributes.includes(translation)) {
          (attributes[translation] = attributes[translation] || []).push(remoteAccount.attributes[attrName]);
        }
      })
    });
    Object.keys(attributes).forEach(attrName => attributes[attrName] = [...new Set(attributes[attrName])].flat());
    const disabledSubmit = !initial && !this.isValid();
    return (
      <div className="mod-attributes">
        <div className="intro">
          <p dangerouslySetInnerHTML={{__html: I18n.t("attributes.title")}}/>
        </div>
        <p className="provided">{I18n.t("attributes.providedByInstitution")}</p>
        {Object.keys(attributes).sort().map(attrName =>
          <InputField
            key={attrName}
            value={attributes[attrName].join(", ")}
            name={attrName}
            disabled={true}
          />
        )}
        <p className="provided last">{I18n.t("attributes.providedByYou")}</p>
        <div className="attributes-form">
          {
            names.map((name, index) =>
              <InputField
                key={index}
                value={name}
                name={I18n.t("attributes.name")}
                index={index}
                placeholder={I18n.t("attributes.namePlaceholder")}
                onChange={this.changeAttr("names", index)}
                toolTip={I18n.t("attributes.nameTooltip")}
              />)
          }
          {(!initial && isEmpty(names.filter(val => !isEmpty(val)))) &&
          <span className="error">{I18n.t("attributes.required", {name: I18n.t("attributes.name")})}</span>}
          {
            emails.map((email, index) =>
              <div>
                <InputField
                  key={index}
                  value={email}
                  name={I18n.t("attributes.email")}
                  index={index}
                  onBlur={this.validateEmail(index)}
                  placeholder={I18n.t("attributes.emailPlaceholder")}
                  onChange={this.changeAttr("emails", index)}
                  toolTip={I18n.t("attributes.emailTooltip")}
                  onAdd={index === 0 ? this.addAttr("emails") : null}
                  onDelete={index !== 0 ? this.deleteAttr("emails", index) : null}
                />
                {invalidInputs[`email${index}`] && <span className="error">
                  {I18n.t("attributes.invalid", {name: I18n.t("attributes.mail").toLowerCase()})}
                </span>}
              </div>)
          }
          {(!initial && isEmpty(emails.filter(val => !isEmpty(val)))) &&
          <span className="error">{I18n.t("attributes.required", {name: I18n.t("attributes.email")})}</span>}

          {
            phones.map((phone, index) =>
              <InputField
                key={index}
                value={phone}
                name={I18n.t("attributes.phone")}
                index={index}
                placeholder={I18n.t("attributes.phonePlaceholder")}
                onChange={this.changeAttr("phones", index)}
                toolTip={I18n.t("attributes.phoneTooltip")}
                onAdd={index === 0 ? this.addAttr("phones") : null}
                onDelete={index !== 0 ? this.deleteAttr("phones", index) : null}
              />)
          }
          <InputField
            value={address}
            name={I18n.t("attributes.address")}
            placeholder={I18n.t("attributes.addressPlaceholder")}
            onChange={this.changeAttr("address")}
            toolTip={I18n.t("attributes.addressTooltip")}
            multiline={true}
          />
          <SelectField value={this.countryOptions.find(option => country === option.value)}
                       options={this.countryOptions}
                       name={I18n.t("attributes.country")}
                       toolTip={I18n.t("attributes.countryTooltip")}
                       clearable={true}
                       searchable={true}
                       placeholder={I18n.t("attributes.countryPlaceholder")}
                       onChange={selectedOption => this.setState({country: selectedOption ? selectedOption.value : null})}
          />
          <SelectField value={this.languageOptions.find(option => refLanguage === option.value)}
                       options={this.languageOptions}
                       name={I18n.t("attributes.refLanguage")}
                       toolTip={I18n.t("attributes.refLanguageTooltip")}
                       clearable={true}
                       searchable={true}
                       placeholder={I18n.t("attributes.refLanguagePlaceholder")}
                       onChange={selectedOption => this.setState({refLanguage: selectedOption ? selectedOption.value : null})}
          />
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