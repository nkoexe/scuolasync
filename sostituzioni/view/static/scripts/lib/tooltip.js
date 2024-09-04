const tooltip = document.querySelector("#tooltip")
const tooltip_arrow = document.querySelector("#tooltip-arrow")
const tooltip_text = document.querySelector("#tooltip-text")

const tooltip_padding = 10

tooltip.onmouseover = () => {
  tooltip_arrow.classList.add("visible")
}

function attach_tooltips() {
  for (const element of document.querySelectorAll('[data-tooltip]')) {
    element.onmouseover = () => {
      tooltip_text.innerHTML = element.dataset.tooltip
      tooltip.classList.remove("tooltip-bottom")

      let rect = element.getBoundingClientRect()
      let tooltip_rect = tooltip.getBoundingClientRect()

      let top = rect.top - tooltip_rect.height
      if (top < 0) {
        top = rect.bottom
        tooltip.classList.add("tooltip-bottom")
      }

      let arrow_padding = 0
      let left = rect.left + rect.width / 2 - tooltip_rect.width / 2

      if (left + tooltip_rect.width + tooltip_padding > window.innerWidth) {
        arrow_padding = left + tooltip_rect.width - window.innerWidth + tooltip_padding
        left = window.innerWidth - tooltip_rect.width - tooltip_padding
      }
      else if (left < tooltip_padding) {
        arrow_padding = left - tooltip_padding
        left = tooltip_padding
      }

      tooltip.style.top = top + "px"
      tooltip.style.left = left + "px"
      tooltip.classList.add("visible")
      tooltip_arrow.style.translate = arrow_padding + "px" + " 0"
    }
    element.onmouseout = () => {
      tooltip.classList.remove("visible")
    }
  }
}