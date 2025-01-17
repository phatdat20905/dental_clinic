document.addEventListener("DOMContentLoaded", () => {
  const dentistSelect = document.getElementById("dentist");
  const dateInput = document.getElementById("date");
  const timeSelect = document.getElementById("time");

  // Lắng nghe sự kiện thay đổi của dentist và date
  dentistSelect.addEventListener("change", updateTimes);
  dateInput.addEventListener("change", updateTimes);

  function updateTimes() {
    const dentistId = dentistSelect.value;
    const date = dateInput.value;

    if (dentistId && date) {
      fetch(`/api/get-available-times?dentist_id=${dentistId}&date=${date}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to fetch times");
          }
          return response.json();
        })
        .then((data) => {
          // Gỡ lỗi - In ra dữ liệu API trả về
          console.log("API Response:", data);

          // Reset danh sách time
          timeSelect.innerHTML = '<option value="">Chọn thời gian</option>';

          if (data.times && data.times.length > 0) {
            // Thêm các thời gian khả dụng
            data.times.forEach((time) => {
              const option = document.createElement("option");
              option.value = time;
              option.textContent = time;
              timeSelect.appendChild(option);
            });
          } else {
            // Hiển thị thông báo không có thời gian khả dụng
            const option = document.createElement("option");
            option.value = "";
            option.textContent = "Không có thời gian khả dụng";
            timeSelect.appendChild(option);
          }
        })
        .catch((error) => {
          console.error("Error fetching times:", error);
          alert("Lỗi khi lấy dữ liệu thời gian!");
        });
    } else {
      console.log("Vui lòng chọn bác sĩ và ngày.");
    }
  }
});
