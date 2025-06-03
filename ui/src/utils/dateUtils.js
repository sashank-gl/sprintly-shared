export function formatDate(dateStr) {
  const date = new Date(dateStr)
  const now = new Date()
  const diffMs = now - date
  const diffMinutes = Math.floor(diffMs / 60000)

  if (diffMinutes < 10) {
    return 'a few minutes ago'
  }

  const isToday =
    date.getDate() === now.getDate() &&
    date.getMonth() === now.getMonth() &&
    date.getFullYear() === now.getFullYear()

  if (isToday) {
    return date
      .toLocaleTimeString([], {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
      })
      .replace(/\s?(am|pm)/i, (match) => match.toUpperCase())
  }

  const yesterday = new Date()
  yesterday.setDate(now.getDate() - 1)
  const isYesterday =
    date.getDate() === yesterday.getDate() &&
    date.getMonth() === yesterday.getMonth() &&
    date.getFullYear() === yesterday.getFullYear()

  if (isYesterday) {
    return `Yesterday ${date
      .toLocaleTimeString([], {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
      })
      .replace(/\s?(am|pm)/i, (match) => match.toUpperCase())}`
  }

  const options = { month: 'short', day: 'numeric' }
  if (date.getFullYear() !== now.getFullYear()) {
    if (date.getFullYear() === now.getFullYear() - 1) {
      return `Last year ${date.toLocaleDateString(undefined, options)} at ${date
        .toLocaleTimeString([], {
          hour: 'numeric',
          minute: '2-digit',
          hour12: true,
        })
        .replace(/\s?(am|pm)/i, (match) => match.toUpperCase())}`
    } else {
      return (
        date.toLocaleDateString(undefined, {
          ...options,
          year: '2-digit',
        }) +
        ' at ' +
        date
          .toLocaleTimeString([], {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true,
          })
          .replace(/\s?(am|pm)/i, (match) => match.toUpperCase())
      )
    }
  }

  return (
    date.toLocaleDateString(undefined, options) +
    ' at ' +
    date
      .toLocaleTimeString([], {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
      })
      .replace(/\s?(am|pm)/i, (match) => match.toUpperCase())
  )
}

export function formatLocalDateOnly(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString()
}

// Always convert ISO datetime strings to yyyy-MM-dd before binding to <input type="date">.

export function formatToCalendarDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}
