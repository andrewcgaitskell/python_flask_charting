
The following is from the original Ruby Version

ActionController::Routing::Routes.draw do |map|
  # The priority is based upon order of creation: first created -> highest priority.

  # Sample of regular route:
  #   map.connect 'products/:id', :controller => 'catalog', :action => 'view'
  # Keep in mind you can assign values other than :controller and :action

  # Sample of named route:
  #   map.purchase 'products/:id/purchase', :controller => 'catalog', :action => 'purchase'
  # This route can be invoked with purchase_url(:id => product.id)

  # Sample resource route (maps HTTP verbs to controller actions automatically):
  #   map.resources :products

  # Sample resource route with options:
  #   map.resources :products, :member => { :short => :get, :toggle => :post }, :collection => { :sold => :get }

  # Sample resource route with sub-resources:
  #   map.resources :products, :has_many => [ :comments, :sales ], :has_one => :seller
  
  # Sample resource route with more complex sub-resources
  #   map.resources :products do |products|
  #     products.resources :comments
  #     products.resources :sales, :collection => { :recent => :get }
  #   end

  # Sample resource route within a namespace:
  #   map.namespace :admin do |admin|
  #     # Directs /admin/products/* to Admin::ProductsController (app/controllers/admin/products_controller.rb)
  #     admin.resources :products
  #   end

  # You can have the root of your site routed with map.root -- just remember to delete public/index.html.
  # map.root :controller => "welcome"

  # See how all your routes lay out with "rake routes"

  # Install the default routes as the lowest priority.
  # Note: These default routes make all actions in every controller accessible via GET requests. You should
  # consider removing or commenting them out if you're using named routes and resources.
  # map.connect ':controller/:action/:id'
  # map.connect ':controller/:action/:id.:format'
  
  map.resources :users
  map.resource :session, :controller => 'session'
  map.resources :limits
    # map.resources :plots do
    #   member do
    #       get :duplicate
    #   end
    # end
  map.resources :plots, :member => {:graph_for => :get, :legend_for => :get}

    #need the replacer route which is a test data example route
  map.replacer '/replacer', :controller => 'limits', :action => 'replacer'
    #these routes are used in the new limit example page
  map.replacer '/ex_label', :controller => 'limits', :action => 'ex_label'
  map.replacer '/ex_comment', :controller => 'limits', :action => 'ex_comment'
  map.replacer '/ex_reference', :controller => 'limits', :action => 'ex_reference'
  map.replacer '/ex_data', :controller => 'limits', :action => 'ex_data'
  map.replacer '/ex_yrescale', :controller => 'limits', :action => 'ex_yrescale'
  map.replacer '/ex_xrescale', :controller => 'limits', :action => 'ex_xrescale'
  map.replacer '/ex_dir', :controller => 'limits', :action => 'ex_dir'
    #that's all of them
    #download routes
  map.download_ex '/download_ex', :controller => 'info', :action => 'download_ex'
  map.download_ex '/download_temp', :controller => 'info', :action => 'download_temp'
    #duplicate route
  map.duplicate '/duplicate', :controller => 'plots', :action => 'duplicate'
    #nominate/recant
  map.nominate '/nominate', :controller => 'limits', :action => 'nominate'
  map.recant '/recant', :controller => 'limits', :action => 'recant'
  map.resources :experiments

  map.faq '/faq', :controller => 'info', :action => 'faq'
  map.whatsnew '/whatsnew', :controller => 'info', :action => 'whatsnew'
    
    
  map.root :controller => 'plots'
  map.signup '/signup', :controller => 'users', :action => 'new'
  map.login '/login', :controller => 'session', :action => 'new'
  map.logout '/logout', :controller => 'session', :action => 'destroy'
  map.activate '/activate/:activation_code', :controller => 'users', :action => 'activate', :activation_code => nil
  map.destroy_all '/destroy_all', :controller => 'plots', :action => 'destroy_all'
  map.admin_edit '/admin_edit', :controller => 'limits', :action => 'admin_edit'
  map.make_official '/make_official', :controller => 'limits', :action => 'make_official'
  map.make_unofficial '/make_unofficial', :controller => 'limits', :action => 'make_unofficial'
  map.update_greatest_hits '/update_greatest_hits', :controller => 'limits', :action => 'update_greatest_hits'
  map.forgot_password '/forgot_password', :controller => 'users', :action => 'forgot_password'
  map.reset_password '/reset_password/:reset_password_code', :controller => 'users', :action => 'reset_password'
  map.forgot_login '/forgot_login', :controller => 'users', :action => 'forgot_login'
  map.resend_activation '/resend_activation', :controller => 'users', :action => 'resend_activation'
  map.with_options :controller => 'info' do |info|
    info.privacy 'privacy', :action => 'privacy'
    info.contact 'contact', :action => 'contact'
    info.contact 'example', :action => 'example'
    info.help 'help', :action => 'help'
  end
  map.simple_captcha '/simple_captcha/:action', :controller => 'simple_captcha'
  map.update_limit_disp '/update_limit_disp', :controller => 'plots', :action => 'update_limit_disp'
end
