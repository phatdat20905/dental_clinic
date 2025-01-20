document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        // Lấy giá trị từ các trường input
        const fullName = document.getElementById("full_name").value.trim();
        const date = document.getElementById("date").value;
        const time = document.getElementById("time").value;
        const phone = document.getElementById("phone").value.trim();
        const address = document.getElementById("address").value.trim();
        // Kiểm tra các trường nhập liệu
        if (fullName === "" || date === "" || time === "" || phone === "" || address === "") {
            alert("Vui lòng điền đầy đủ thông tin!");
            return;
        }
        // Kiểm tra định dạng số điện thoại (10 chữ số)
        const phoneRegex = /^[0-9]{10}$/;
        if (!phoneRegex.test(phone)) {
            alert("Số điện thoại không hợp lệ! Vui lòng nhập 10 chữ số.");
            return;
        }
        // Gửi form nếu tất cả điều kiện hợp lệ
        alert("Bạn đã đặt lịch thành công !");
        form.submit();
    });
});
