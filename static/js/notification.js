function checkAllNotification(){
    var url = "{% url 'checkAllNotification' %}"
    $.ajax({
      url: url,
      dataType:'json',
      type:'GET',
      async:false,
      success:function(data){
      }
    });
    location.reload();
    return true;
  }
  
  
  
function checkNotification(notification_id){
    var id = notification_id;
    var url = "{% url 'checkNotification' 0 %}";
    $.ajax({
      url: url.replace('0', id),
      dataType:'json',
      type:'GET',
      async:false,
      success:function(data){
      }
    });
    
    return true;
}