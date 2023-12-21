 $(document).ready(function(){
  // -[Prediksi Model]---------------------------
  // Fungsi untuk memanggil API ketika tombol prediksi ditekan
  $("#prediksi_submit").click(function(e) {
    e.preventDefault();
    var input_gender = $("gender").val(); 
    var input_age = $("age").val(); 
    var input_weight = $("weight").val(); 
    var input_height = $("height").val(); 
	// Panggil API dengan timeout 1 detik (1000 ms)
    setTimeout(function() {
	  try {
			$.ajax({
			  url  : "/api/prediksi",
			  type : "POST",
			  data : {
          "age":input_age,
          "height": input_height,
          "weight":input_weight,
          "bmi":bmi,
        },

			  success:function(res){
				res_data_prediksi   = res['calculate_bmi']
        
          console.log(res_data_prediksi)
          console.log('test data rekomendasi \n', res_data_rekomendasi)
				// Tampilkan hasil prediksi ke halaman web
			    generate_prediksi(res_data_prediksi);
			  }
			});
		}
		catch(e) {
			// Jika gagal memanggil API, tampilkan error di console
			console.log("Gagal !");
			console.log(e);
		} 
    }, 1000)
    
  })
  } 
)
  