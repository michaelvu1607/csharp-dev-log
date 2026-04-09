using coupling;

var order1 = new Order(new EmailSender());
order1.PlaceOrder();

var order2 = new Order(new SmsSender());
order2.PlaceOrder();