class Popup {
  constructor({ query }) {
    this.element = document.querySelector(query);
    this.isOpen = false;
  }

  toggle() {
    if (this.isOpen) {
      this.close();
    } else {
      this.open();
    }
  }

  open() {
    this.element.classList.add("open");
    this.isOpen = true;
    document.addEventListener('click', this.handleOutsideClick.bind(this));
    document.addEventListener('keydown', this.handleEscapeKey.bind(this));
  }

  close() {
    this.element.classList.remove("open");
    this.isOpen = false;
    document.removeEventListener('click', this.handleOutsideClick.bind(this));
    document.removeEventListener('keydown', this.handleEscapeKey.bind(this));
  }

  handleOutsideClick(e) {
    if (!this.element.contains(e.target) &&
      e.target !== this.element) {
      this.close();
    }
  }

  handleEscapeKey(e) {
    if (e.key === 'Escape') {
      this.close();
    }
  }
}