import React from "react";
import {redirectKey} from "../api";
import I18n from "i18n-js";
import "./Finish.scss";
import Button from "../components/Button";


class Finish extends React.Component {
  constructor(props, context) {
    super(props, context);
    this.state = {
      redirect: "",
    };
  }

  componentDidMount() {
    redirectKey().then(res => {
      this.setState({redirect: res.redirect_url});
    });
  }


  submit = () => {
    window.location.href = this.state.redirect;
  };

  render() {
    const {redirect} = this.state;
    return (
      <div className="mod-finish">
        <div className="intro">
          <p dangerouslySetInnerHTML={{__html: I18n.t("finish.title", {redirectUrl: redirect})}}/>
        </div>
        <section className="actions">
          <Button txt={I18n.t("finish.update")}
                  onClick={this.submit}/>
        </section>
      </div>);

  }
  ;
}

export default Finish;