import I18n from "i18n-js";

I18n.translations.en = {

  header: {
    title: "Account Registry",
    links: {
      help: "Help",
      helpUrl: "https://github.com/SURFscz/SBS/wiki"
    },
  },
  navigation: {
    registration: "Registration",
    account: "Account",
  },
  forms: {
    submit: "Add",
    cancel: "Cancel",
    showMore: "More",
    hideSome: "Less",
    today: "Today",
    manage: "Overview",
    invalidInput: "Invalid input for {{name}}"
  },

  registration: {
    title: "The service that you were trying to reach is part of the eduTEAMS ecosystem. You will need to register here before continuing to the service.",
    agreeToService: "Agree to Service",
    agreeToServiceIcon: "link",
    verify: "Verify personal data",
    verifyIcon: "book",
    validate: "Validate email",
    validateIcon: "gavel",
    registration: "Registration consists out of three steps:",
    agreeToServiceStep: "Agreeing to the eduTEAMS term of service",
    verifyStep: "Verifying your personal data",
    validateStep: "Validating your email",
    continueToService: "Continue to Term of Service",
  },
  aup: {
    title1: "In ourder to use the eduTEAMS services, you need to agree to a number of rules and regulations.<br>These are explained in the document below.",
    title2: "For more information and explanations, you can contact <a href='mailto:boss@eduteams.org'>boss@eduteams.org</a>.",
    title3: "Please read the document and if agreed check the box and proceed to the validation of your personal information",
    downloadPdf: "Download Acceptable Usage Policy (pdf)",
    agreeWithTerms: "I agree with the Acceptable Usage Policy",
    continueToValidation: "Proceed to personal data"
  },
  attributes: {
    title: "Please enter your details. Some have already been provided by your institution.",
    name: "Name",
    namePlaceholder: "Your name",
    nameTooltip: "Your official registered names.",
    email: "Email",
    emailPlaceholder: "Your email",
    emailTooltip: "Your emails. You will receive a confirmation code for each mail you add.",
    phone: "Phone",
    phonePlaceholder: "Your telephone number",
    phoneTooltip: "Your telephone numbers.",
    address: "Address",
    addressPlaceholder: "Your address",
    addressTooltip: "Your primary address.",
    country: "Country",
    countryPlaceholder: "Your country",
    countryTooltip: "The primary country you reside in.",
    refLanguage: "Pref. language",
    refLanguagePlaceholder: "Your Prefered language",
    refLanguageTooltip: "The primary language you would prefer.",
    providedByInstitution: "Provided by your institution.",
    providedByYou: "Provided by you.",
    update: "Continue to validation",
    required: "{{name}} is required",
    commonName: "Name",
    displayName: "Name",
    mail: "Email",
    surName: "Sur name",
    givenName: "Given name",
    isMemberOf: "Groups",
    eduPersonTargetedID: "eduPersonTargetedID",
    eduPersonEntitlement: "Entitlements",
    invalid: "Invalid {{name}}"
  },
  validations: {
    title: "In order to continue all non-verified emails need to be validated.",
    confirmation: "We have sent a verification code to each of the emails.<p/> Please enter the code from the email in the corresponding box.",
    verifiedByProvider: "Verified by your institution",
    verifiedByCode: "Verified by email code",
    enterCode: "Enter code",
    verify: "Verify",
    deleteEmail: "Delete",
    update: "Continue to confirmation",
    validationError: "The code you entered is not correct. Do you wish a new code is sent to this email address?",
    regenerate: "Resend"
  },
  finish: {
    title: "Thank you for registering with eduTEAMS.<p/><p/>More information can be found at <a target='_blank' rel='noopener noreferrer' href='https://eduteams.org'>https://eduteams.org</a>.<p/><p/>You will now be redirected to your destination {{redirectUrl}}",
    update: "Finish registration"
  },
  error_dialog: {
    title: "Unexpected error",
    body: "This is embarrassing; an unexpected error has occurred. It has been logged and reported. Please try again...",
    ok: "Close"
  },
  not_found: {
    title: "404",
    description_html: "The requested page could not be found",
    loginLink: "LOGIN"
  },
  footer: {
    product: "Powered by SCZ",
    productLink: "https://wiki.surfnet.nl/display/SCZ/Science+Collaboration+Zone+Home",
    privacy: "Terms & Privacy",
    privacyLink: "https://wiki.surfnet.nl/display/SCZ/SCZ+Privacy+Policy"
  }
};

export default I18n.translations.en;
