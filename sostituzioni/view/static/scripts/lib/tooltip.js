const tooltip = document.createElement("div")
tooltip.id = "tooltip"
document.body.appendChild(tooltip)

const tooltip_arrow = document.createElement("div")
tooltip_arrow.id = "tooltip-arrow"
tooltip.appendChild(tooltip_arrow)

const tooltip_content = document.createElement("div")
tooltip_content.id = "tooltip-content"
tooltip.appendChild(tooltip_content)

const tooltip_text = document.createElement("span")
tooltip_text.id = "tooltip-text"
tooltip_content.appendChild(tooltip_text)

const tooltip_padding = 10


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