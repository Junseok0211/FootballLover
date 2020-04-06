var go_payment = function (amount, pay_method, playground, user_name, user_phone) {

    return new Promise(function (resolve, reject) {

        // 결제 시작
        IMP.init("imp74044399");

        IMP.request_pay({ // param
            pg: "inicis",
            pay_method: pay_method,
            merchant_uid: "footballlover_" + new Date().getTime(),
            name: playground + " 대관",
            amount: amount,
            buyer_name: user_name,
            buyer_tel: user_phone
        }, function (rsp) { // callback
            if (rsp.success) {
                resolve("SUCCESS");
            } else {
                reject("FAIL");
            }
        });

    });

};