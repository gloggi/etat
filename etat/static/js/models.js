
(function() {
  var _sync = Backbone.sync;
  Backbone.sync = function(method, model, options){
    options.beforeSend = function(xhr){
      var token = $.cookie('csrftoken');
      xhr.setRequestHeader('X-CSRFToken', token);
    };
    return _sync(method, model, options);
  };
})();

Etat.Models.Member = Backbone.Model.extend({

});

Etat.Collections.Members = Backbone.Collection.extend({
    model: Etat.Models.Member,
    url: '/api/members/'
});


