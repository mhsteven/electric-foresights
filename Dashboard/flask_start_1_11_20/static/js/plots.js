document.getElementsByClassName("chart_text1")[0].style.visibility='hidden';
document.getElementById("chart_text2").style.visibility='hidden';


$('#save_value').click(function(){
        var val = '';
        var shave_rate=$('#shave_rate').val();
        var hour_rate=$('#hourlyqty').val();
        val = val+shave_rate+'|'+hour_rate+'|'+$('#workhours').val()+'|'+$('#topN').val()+'|'+$('#leastM').val()+'|';

        $(':checkbox:checked').each(function(i){
          val = val+$(this).val()+'|';
        });
        console.log(val);
        $.ajax({
            url: "/simulator/simulation",
            type: "GET",
            contentType: 'application/json;charset=UTF-8',
            data: {
                'selected': val

            },
            dataType:"json",
            success: function (data) {
                console.log(data);
                Plotly.newPlot('simchart1', data['chart'] );
                document.getElementById("chart_text2").innerHTML = data['msg'];
                document.getElementsByClassName("chart_text1")[0].style.visibility='visible';
                document.getElementById("chart_text2").style.visibility='visible';
                document.getElementById("simchart1").style.visibility='visible';

            }
        });
});

$('#uncheck').click(function(){
   $(':checkbox:checked').prop('checked',false);
   document.getElementsByClassName("chart_text1")[0].style.visibility='hidden';
   document.getElementById("chart_text2").style.visibility='hidden';
   document.getElementById("simchart1").style.visibility='hidden';



});
$('#checkall').click(function(){
   $(':checkbox:not(:checked)').prop('checked',true);
   document.getElementsByClassName("chart_text1")[0].style.visibility='hidden';
   document.getElementById("chart_text2").style.visibility='hidden';
   document.getElementById("simchart1").style.visibility='hidden';

});
