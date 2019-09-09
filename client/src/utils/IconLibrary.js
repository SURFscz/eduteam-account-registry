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
  faCircle
} from '@fortawesome/free-solid-svg-icons'

export function addIcons() {
  library.add(faGavel, faLink, faBook, faCircle, faCheck, faInfoCircle, faInfo, faPlus, faTrash);
}
