

export function formatDate(date_string){
  const date = new Date(date_string);

  // toLocaleStringを使用して、英語（アメリカ）のロケールで整形
  // 秒を表示しないようにオプションを指定
  return date.toLocaleString('en-US', {
    year: 'numeric',    // 年 (例: 2025)
    month: 'long',      // 月 (例: August)
    day: 'numeric',     // 日 (例: 1)
    hour: 'numeric',    // 時 (例: 4 PM)
    minute: '2-digit',  // 分 (例: 46)
    hour12: true        // 12時間表記 (AM/PM)
  });
}


export function validateImage(file) {
  if (!file) {
    return 'Please select a file.';
  }

  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
  if (!allowedTypes.includes(file.type)) {
    return 'Invalid file type. Only JPEG, PNG, and GIF formats are allowed.';
  }

  const maxSizeInBytes = 2 * 1024 * 1024;
  if (file.size > maxSizeInBytes) {
    const maxSizeInMB = Math.round(maxSizeInBytes / 1024 / 1024);
    return `File is too large. The maximum file size is ${maxSizeInMB}MB.`;
  }
  return null;
}

