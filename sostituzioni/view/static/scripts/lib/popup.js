class Popup {
  constructor({ query }) {
    this.element = document.querySelector(query);
    this.isOpen = false;

    this.boundHandleOutsideClick = this.handleOutsideClick.bind(this);
    this.boundHandleEscapeKey = this.handleEscapeKey.bind(this);

    // Create event target for custom events
    this.eventTarget = new EventTarget();
  }

  addEventListener(type, listener, options) {
    this.eventTarget.addEventListener(type, listener, options);
  }

  removeEventListener(type, listener, options) {
    this.eventTarget.removeEventListener(type, listener, options);
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
    document.addEventListener('keydown', this.boundHandleEscapeKey);

    // Delay adding the click handler until the next event cycle
    // This prevents the current click event from closing the popup
    setTimeout(() => {
      document.addEventListener('click', this.boundHandleOutsideClick);
    }, 0);

    this.eventTarget.dispatchEvent(new CustomEvent('open'));
  }

  close() {
    this.element.classList.remove("open");
    this.isOpen = false;
    document.removeEventListener('click', this.boundHandleOutsideClick);
    document.removeEventListener('keydown', this.boundHandleEscapeKey);

    this.eventTarget.dispatchEvent(new CustomEvent('close'));
  }

  handleOutsideClick(e) {
    if (!this.element.contains(e.target) &&
      e.target !== this.element) {
      e.stopPropagation();
      this.close();
    }
  }

  handleEscapeKey(e) {
    if (e.key === 'Escape') {
      this.close();
    }
  }
}