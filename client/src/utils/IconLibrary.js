import {library} from '@fortawesome/fontawesome-svg-core'
import {
  faBook,
  faGavel,
  faInfo,
  faInfoCircle,
  faLink,
  faCheck,
  faPlus,
  faTrash,
  faCircle,
  faEnvelopeOpen,
  faEnvelope
} from '@fortawesome/free-solid-svg-icons'

export function addIcons() {
  library.add(faGavel, faLink, faBook, faEnvelopeOpen, faEnvelope, faCircle, faCheck, faInfoCircle, faInfo, faPlus, faTrash);
}
