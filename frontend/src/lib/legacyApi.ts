export const postQuestionXHR = (content: string, token: string | null): Promise<any> => {
  return new Promise((resolve, reject) => {
    if (!content || content.trim() === "") {
        reject(new Error("Validation Error: Question cannot be blank."));
        return;
    }
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

    const xhr = new XMLHttpRequest();
    xhr.open("POST", `${apiUrl}/questions/`, true);
    
    xhr.setRequestHeader("Content-Type", "application/json");
    if (token) {
        xhr.setRequestHeader("Authorization", `Bearer ${token}`);
    }

    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        if (xhr.status >= 200 && xhr.status < 300) {
          try {
            const response = JSON.parse(xhr.responseText);
            resolve(response);
          } catch (e) {
            reject(new Error("Failed to parse response"));
          }
        } else {
          reject(new Error(xhr.statusText || "Request failed"));
        }
      }
    };

    xhr.onerror = function () {
      reject(new Error("Network Error"));
    };

    const data = JSON.stringify({ content: content });
    xhr.send(data);
  });
};