import React from 'react';
import ReactDOM from 'react-dom';
import { Button } from 'reactstrap';
import { gettext } from './utils/constants';
import Logo from './components/logo';
import Account from './components/common/account';
import TermsPreviewWidget from './components/terms-preview-widget';

import './css/tc-accept.css';

const { csrfToken } = window.app.pageOptions;
const {
  termsName,
  formAction,
  formTerms,
  formReturnTo,
  logoutURL,
  termsText
} = window.tc;


class TCAccept extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isChecked: false
    }

    this.handleCheckboxChanged = this.handleCheckboxChanged.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleCheckboxChanged(event) {
    this.setState({
      isChecked: event.target.checked
    });
    
  }

  handleSubmit(event) {
    
    if (!this.state.isChecked) {
      event.preventDefault();
      return false;
    }
  }

  render() {
    return (
      <div className="h-100 d-flex flex-column">
        <div className="top-header d-flex justify-content-between">
          <Logo />
          <Account />
        </div>
        <div className="o-auto">
          <div className="py-4 px-4 my-6 mx-auto content">
            <h2 dangerouslySetInnerHTML={{__html: termsName}}></h2>
            <div className="article">
              <TermsPreviewWidget content={termsText} />
            </div>
            <form action={formAction} method="post" onSubmit={this.handleSubmit}>
              <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
              <div dangerouslySetInnerHTML={{__html: formTerms}}></div>
              <div dangerouslySetInnerHTML={{__html: formReturnTo}}></div>
              <div>
                <input type="checkbox" name="agreeTC" checked={this.state.isChecked} onChange={this.handleCheckboxChanged}/>
                <label htmlFor="agreeTC" className='checkbox-label'>I agree</label>
              </div>
              <Button type="submit" disabled={!this.state.isChecked} >{gettext('Accept')}</Button>
              <a href={logoutURL} className="btn btn-secondary ml-2">{gettext('Cancel')}</a>
            </form>
          </div>
        </div>
      </div>
    );
  }
}

ReactDOM.render(
  <TCAccept />,
  document.getElementById('wrapper')
);
