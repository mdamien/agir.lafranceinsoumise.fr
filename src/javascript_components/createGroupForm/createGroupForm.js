import axios from '../lib/axios';
import 'babel-polyfill';
import React from 'react';
import ReactDOM from 'react-dom';
import Cleave from 'cleave.js/react';
import CleavePhone from 'cleave.js/dist/addons/cleave-phone.fr';
import {PhoneNumberUtil, PhoneNumberFormat} from 'google-libphonenumber';
import StepZilla from 'react-stepzilla';
import 'react-stepzilla/src/css/main.css';
import qs from 'querystring';

import NavSelect from '../lib/navSelect';
import './createGroupForm.css';

const countries = require('localized-countries')(require('localized-countries/data/fr'));
const phoneUtil = PhoneNumberUtil.getInstance();

const apiEndpoint = API_ENDPOINT; // defined by webpack

const groupLabels = {
  L: 'Un groupe d\'action local',
  P: 'Un groupe d\'action professionnel',
  F: 'Un groupe d\'action fonctionnel',
  B: 'Un groupe d\'action thématique',
};

class CreateGroupForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {fields: {}};
    this.setFields = this.setFields.bind(this);
  }

  async componentDidMount() {
    let subtypes = (await axios.get(apiEndpoint + '/groups_subtypes/')).data;
    this.setState({subtypes});

  }

  setFields(fields) {
    this.setState({fields: Object.assign(this.state.fields, fields)});
  }

  render () {
    if (!this.state.subtypes) {
      return null;
    }

    let steps = [
      {name: 'Un groupe pour quoi ?', component: <GroupTypeStep setFields={this.setFields} subtypes={this.state.subtypes} />},
      {name: 'Informations de contact', component: <ContactStep setFields={this.setFields} />},
      {name: 'Localisation', component: <LocationStep setFields={this.setFields} />},
      {name: 'Validation et nom', component: <ValidateStep fields={this.state.fields} />},
    ];

    return (
      <div className="step-progress">
        <StepZilla steps={steps} stepsNavigation={false} showNavigation={false} preventEnterSubmission={true} />
      </div>
    )
  }
}

class FormStep extends React.Component {
  constructor(props) {
    super(props);
    this.setFields = props.setFields;
    this.jumpToStep = props.jumpToStep;
    this.state = {errors: {}};
  }
}

class GroupTypeStep extends FormStep {
  constructor(props) {
    super(props);
    this.allSubtypes = props.subtypes;
    this.confirm = this.confirm.bind(this);
    this.onSubtypeChange = this.onSubtypeChange.bind(this);
    this.setType = this.setType.bind(this);
  }

  setType(type) {
    this.subtypes = this.allSubtypes
      .filter(s => s.type === type)
      .map(subtype => ({value: subtype.label, label: subtype.description}));
    if (this.subtypes.length < 2) {
      this.setFields({type, subtypes: this.subtypes});
      this.jumpToStep(1);

      return;
    }

    this.setState({type});
  }

  onSubtypeChange(subtypes) {
    this.setState({subtypes});
  }

  confirm() {
    this.setFields({type: this.state.type, subtypes: this.state.subtypes});
    this.jumpToStep(1);
  }

  render() {
    if (!this.state.type) {
      return (
        <div className="row padtopmore">
          <div className="col-sm-6">
            <h4>Quel type de groupe voulez-vous créer ?</h4>
            <blockquote>
              <p>
                &laquo;&nbsp;Chaque insoumis.e peut créer ou rejoindre un ou plusieurs groupes d’action dès lors
                qu’il respecte le cadre et la démarche de la France insoumise dans un esprit
                d’ouverture, de bienveillance et de volonté de se projeter dans l’action.&nbsp;&raquo;
              </p>
              <footer>
                <a href="https://lafranceinsoumise.fr/groupes-appui/charte-groupes-dappui-de-france-insoumise/">
                  Charte des groupes d’action de la France insoumise
                </a>
              </footer>
            </blockquote>
            <p>
              La <a href="https://lafranceinsoumise.fr/groupes-appui/charte-groupes-dappui-de-france-insoumise/">
              Charte des groupes d’action de la France insoumise</a> définit quatres types de groupes différents.
            </p>
            <p>
              Ces groupes répondent à des besoins différents. Vous pouvez parfaitement participer à plusieurs groupes
              en fonction de vos intérêts.
            </p>
          </div>
          <div className="col-sm-6 padbottom">
            <h4>Je veux créer...</h4>
            <button className="btn btn-default btn-block padbottom" style={{whiteSpace: 'normal'}} onClick={() => this.setType('L')}>
              <h4>{groupLabels['L']}</h4>
              <p>Les groupes d’action géographiques sont constitués sur la base d’un territoire réduit (quartier,
                villages ou petites villes, cantons) et non à l’échelle d’une région, d’un département, d’une
                circonscription électorale ou d’une grande ville. Chaque insoumis⋅e ne peut assurer l’animation
                que d’un seul groupe d’action géographique.</p>
            </button>
            <button className="btn btn-default btn-block padbottom" style={{whiteSpace: 'normal'}} onClick={() => this.setType('P')}>
              <h4>{groupLabels['P']}</h4>
              <p>Les groupes d’action professionnels rassemblent des insoumis⋅es qui souhaitent agir au sein de leur
                entreprise ou de leur lieu d’étude.</p>
            </button>
            <button className="btn btn-default btn-block padbottom" style={{whiteSpace: 'normal'}} onClick={() => this.setType('F')}>
              <h4>{groupLabels['F']}</h4>
              <p>Les groupes d’action fonctionnels sont des groupes d’action transversaux autour de fonctions précises
                (mise en place de formation, organisation des apparitions publiques, rédaction de tracts,
                chorale insoumise, journaux locaux, auto-organisation, etc…).</p>
            </button>
            <button className="btn btn-default btn-block padbottom" style={{whiteSpace: 'normal'}} onClick={() => this.setType('B')}>
              <h4>{groupLabels['B']}</h4>
              <p>
                Les groupes d’action thématiques réunissent des insoumis⋅es qui souhaitent agir de concert sur un thème
                donné en lien avec les livrets thématiques correspondant.
              </p>
            </button>
          </div>
        </div>
      );
    }

    return (
      <div className="row padtopmore">
        <div className="col-responsive">
          <p>Choisissez maintenant les thèmes qui vous intéressent.</p>
          <NavSelect onChange={this.onSubtypeChange} choices={this.subtypes} max={3} />
          <button className="btn btn-primary" onClick={this.confirm}>Suivant</button>
        </div>
      </div>
    );
  }
}

class ContactStep extends FormStep {
  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    event.preventDefault();

    let phone = this.phone.value;
    let phoneValid = false;
    try {
      let phoneNumber = phoneUtil.parse(phone, 'FR');
      phoneValid = phoneUtil.isValidNumber(phoneNumber);
      phone = phoneUtil.format(phoneNumber, PhoneNumberFormat.E164)
    } catch (e) {
      phoneValid = false;
    }

    if (!phoneValid) {
      return this.setState({errors: {phone: 'Vous devez entrer un numéro de téléphone valide.'}});
    }

    this.setFields({phone, email: this.email.value, hidePhone: this.hidePhone.value});
    this.jumpToStep(2);
  }

  render() {
    return (
      <div className="row padtopmore">
        <div className="col-md-6">
          <h4>Informations de contact</h4>
          <p>
            Ces informations sont les informations de contact du groupe. Vous devez indiquer une adresse email et un
            numéro de téléphone. Ce ne sont pas forcément vos informations de contact personnelles&nbsp;: en particulier,
            l'adresse email peut appartenir au groupe et être relevée par plusieurs personnes.
          </p>
          <p>
            Vous pouvez ne pas rendre le numéro de téléphone public (surtout si c'est votre numéro personnel).
            Néanmoins, il est obligatoire de le fournir pour que la coordination des groupes d'action puisse vous
            contacter.
          </p>
          <a className="btn btn-default" onClick={() => this.jumpToStep(0)}>&larr;&nbsp;Précédent</a>
        </div>
        <div className="col-md-6">
          <form onSubmit={this.handleSubmit}>
            <div className="form-group">
              <label>Adresse email du groupe</label>
              <input className="form-control" ref={i => this.email = i} type="email" />
            </div>
            <label>Numéro de téléphone du contact</label>
            <div className="row">
              <div className="col-md-6">
                <div className={'form-group' + (this.state.errors.phone ? ' has-error' : '')}>
                  <Cleave options={{phone: true, phoneRegionCode: 'FR'}} htmlRef={(i => this.phone = i)} className="form-control"  />
                  {this.state.errors.phone ? (<span className="help-block">{this.state.errors.phone}</span>) : ''}
                </div>
              </div>
              <div className="col-md-6">
                <div className="checkbox">
                  <label>
                    <input ref={i => this.hidePhone = i} type="checkbox"/> Ne pas rendre public
                  </label>
                </div>
              </div>
            </div>
            <button className="btn btn-primary" type="submit">Suivant&nbsp;&rarr;</button>
          </form>
        </div>
      </div>
    );
  }
}

class LocationStep extends FormStep {
  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    event.preventDefault();

    this.setFields({
      locationName: this.locationName.value,
      locationAddress1: this.locationAddress1.value,
      locationAddress2: this.locationAddress2.value,
      locationZip: this.locationZip.value,
      locationCity: this.locationCity.value,
      locationCountryCode: this.locationCountryCode.value,
    });
    this.jumpToStep(3);
  }

  render() {
    return (
      <div className="row padtopmore">
        <div className="col-md-6">
          <h4>Localisation</h4>
          <p>
            Merci d'indiquer une adresse précise avec numéro de rue, sans quoi le groupe n'apparaîtra pas sur la carte.
          </p>
          <p>
            Si les réunions se déroulent chez vous et que vous ne souhaitez pas rendre cette adresse publique, vous pouvez
            indiquer un endroit à proximité, comme un café, ou votre mairie.
          </p>
          <a className="btn btn-default" onClick={() => this.jumpToStep(1)}>&larr;&nbsp;Précédent</a>
        </div>
        <div className="col-md-6">
          <form onSubmit={this.handleSubmit}>
            <div className="form-group">
            <label>Nom du lieu</label>
              <input ref={i => this.locationName = i} placeholder="Exemple: café de la gare, rue des postes..." className="form-control" type="text" required />
            </div>
            <div className="form-group">
              <label className="control-label">Adresse</label>
              <input ref={i => this.locationAddress1 = i} placeholder="1ère ligne" className="form-control" type="text" required />
              <input ref={i => this.locationAddress2 = i} placeholder="2ème ligne" className="form-control" type="text" />
            </div>
            <div className="row">
              <div className="col-md-4">
                <div className="form-group">
                  <label className="control-label">Code postal</label>
                  <input ref={i => this.locationZip = i} className="form-control" type="text" required />
                </div>
              </div>
              <div className="col-md-8">
                <div className="form-group">
                  <label className="control-label">Ville</label>
                  <input ref={i => this.locationCity = i} className="form-control" type="text" required />
                </div>
              </div>
            </div>
            <div className="form-group">
              <label className="control-label">Pays</label>
              <select ref={i => this.locationCountryCode = i} className="form-control" required defaultValue='FR'>
                {countries.array().map(country => (<option value={country.code} key={country.code}>{country.label}</option>))}
              </select>
            </div>
            <button className="btn btn-primary" type="submit">Suivant&nbsp;&rarr;</button>
          </form>
        </div>
      </div>
    );
  }
}

class ValidateStep extends FormStep {
  constructor(props) {
    super(props);
    this.post = this.post.bind(this);
    this.state = {fields: props.fields};
  }

  async post(e) {
    e.preventDefault();

    let data = qs.stringify({
      name: this.groupName.value,
      contact_email: this.state.fields.email,
      contact_email: this.state.fields.email,
      contact_phone: this.state.fields.phone,
      contact_hide_phone: this.state.fields.hidePhone,
      location_name: this.state.fields.locationName,
      location_address1: this.state.fields.locationAddress1,
      location_adcress2: this.state.fields.locationAddress2 || null,
      location_zip: this.state.fields.locationZip,
      location_city: this.state.fields.locationCity,
      location_country: this.state.fields.locationCountryCode,
      type: this.state.fields.type,
      subtypes: this.state.fields.subtypes.map(subtype => subtype.value),
    });

    try {
      let res = await axios.post('form/', data);
      location.href = res.data.url;
    } catch (e) {
      this.setState({error: e});
    }
  }

  render() {
    return (
      <div className="row padtopmore">
        <div className="col-md-6">
          <p>Voici les informations que vous avez entrées.</p>
          <ul>
            <li>
              <strong>Type de groupe&nbsp;:</strong> {groupLabels[this.state.fields.type]}
            </li>
            <li>
              <strong>Numéro de téléphone&nbsp;:</strong> {this.state.fields.phone} ({this.state.fields.hidePhone === 'on' ? 'caché' : 'public'})
            </li>
            <li>
              <strong>Adresse email du groupe&nbsp;:</strong> {this.state.fields.email}
            </li>
            <li>
              <strong>Lieu&nbsp;:</strong><br/>
              {this.state.fields.locationAddress1}<br />
              {this.state.fields.locationAddress2 ? <span>{this.state.fields.locationAddress2}<br /></span> : ''}
              {this.state.fields.locationZip}, {this.state.fields.locationCity}
            </li>
          </ul>
          <a className="btn btn-default" onClick={() => this.jumpToStep(2)}>&larr;&nbsp;Précédent</a>
        </div>
        <div className="col-md-6">
          <p>Pour finir, il vous reste juste à choisir un nom pour votre groupe&nbsp;! Choisissez un nom simple
          et descriptif (par exemple : &laquo;&nbsp;Groupe d'action de la Porte d'Arras&nbsp;&raquo;).</p>
          <form onSubmit={this.post}>
            <div className="form-group">
              <input className="form-control" ref={i => this.groupName = i} type="text" placeholder="Nom du groupe" required />
            </div>
            <button className="btn btn-primary" type="submit">Créer mon groupe</button>
          </form>
          { this.state.error && (
            <div className="alert alert-warning">
              Un erreur s'est produite. Merci de réessayer plus tard.
            </div>
          ) }
        </div>
      </div>
    );
  }
}

export default CreateGroupForm;