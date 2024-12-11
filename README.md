# Mikrotik Script

------

#### I. Tạo list address WAN

1. Tạo Profiles mới để dùng script,có thể dùng luôn Profiles defautl cũng được nhưng nên tạo mới tránh lỗi còn xóa đi mà làm lại được

2. PPP --> Profiles --> defautl --> Copy --> Điền tên mới(mình đặt là connect) --> Apply
   ![1](img/1.png)

3. PPP --> Interface --> pppoe-out1 --> Dial Out --> Profile --> Chọn Profile đã tạo ở bước trên(có bao nhiêu pppoe thì làm lần lượt,như nhà mình 2 pppoe thì mình làm cả 2) --> Apply
   ![2](img/2.png)

4. PPP --> Profiles --> connect(tên profile đã tạo ở bước trên) --> Scripts --> Điền code dưới --> Apply

   ```Code
   :delay 5
   /ip firewall address-list remove [/ip firewall address-list find list=WAN]
   
   :local wanip [/ip address get [/ip address find where interface=pppoe-out1] address];
   :set wanip [:pick $wanip 0 ([:len $wanip]-3) ];
   :put $wanip;
   /ip firewall address-list add list=WAN address=$wanip
   ```

   ![3](img/3.png)

5. Ngắt kết nối PPPOE rồi kết nối lại,kiểm tra IP --> Firewall --> Address List 
   nếu thấy list WAN có IP WAN là đã thành công,
   ![4](img/4.png)

6. Có thể sử dụng List WAN này để cấu hình Hairpin Nat, Dstnat...
   Với cách này thì luôn update IP WAN vào List WAN nhanh nhất và chính xác nhất, không bị phụ thuộc vào cloud ddns , không phải lòng lòng update ip wan lên ddns rồi lại kéo ip wan từ ddns xuống



#### II.Auto Update IP WAN Lên Cloudflare

1. Đăng nhập vào CF rồi vào [link này](https://dash.cloudflare.com/profile/api-tokens) để tạo Token API

2. Bấm vào Create Token,Chọn Edit zone DNS 
   ![](img/5.png)

   1. Chọn như hình dưới rồi bấm Continue to summary rồi bấm tiếp Create Token và lưu lại Token vì token chỉ xuất hiện 1 lần
      ![](img/6.png)
      ![](img/7.png)
      ![](img/8.png)

   2. Quay lại trang cấu hình DNS của CF, Bấm F12, chọn sang tab Network, chọn tên miền cần update ip, bấm edit, rồi bấm save, sẽ cho ra kết qua như hình dưới, chú ý tới bên cột NAME cái hàng chỉ có số và chữ, bấm vào sẽ hiển thị 1 tab mới,để ý dòng Request URL
       ![](img/9.png)
      ![](img/10.png)
      ![](img/11.png)
      ![](img/12.png)

   3. Ví dụ như của mình dòng Request URL như sau:
      `https://dash.cloudflare.com/api/v4/zones/6df64070exxxxxxx67f2602fd6f3d/dns_records/cd27cbb6b039c05xxxxx7978ef6c9c9`

   4. Chỉnh sửa Script sau,thay tenmiencuaban , yyyyy, và tokencuaban cho đúng,Chú ý copy từ chỗ v4 thay vào nhé: /v4/zones/6df64070exxxxxxx67f2602fd6f3d/dns_records/cd27cbb6b039c05xxxxx7978ef6c9c9

      ```
      :local wanip [/ip address get [/ip address find where interface=pppoe-out1] address];
      :set wanip [:pick $wanip 0 ([:len $wanip]-3)];
      :put $wanip;
      /tool fetch http-data="{\"type\":\"A\",\"name\":\"tenmiencuaban\",\"content\":\"$wanip\",\"ttl\":60,\"proxied\":false}" url="https://api.cloudflare.com/client/yyyyyyy" http-method=put mode=https keep-result=no http-header-field="Authorization: Bearer tokencuaban, Content-Type: application/json"
      ```

   5. Sau khi thay xong thì nó có dạng như bên dưới

      ```
      :local wanip [/ip address get [/ip address find where interface=pppoe-out1] address];
      :set wanip [:pick $wanip 0 ([:len $wanip]-3)];
      :put $wanip;
      /tool fetch http-data="{\"type\":\"A\",\"name\":\"abc.com\",\"content\":\"$wanip\",\"ttl\":60,\"proxied\":false}" url="https://api.cloudflare.com/client/v4/zones/6df64070e5e674xxxx2602fd6f3d/dns_records/cd27cbb6b039xxxx7978ef6c9c9" http-method=put mode=https keep-result=no http-header-field="Authorization: Bearer PQPoNHXZDHxxxxBl-HlZJ-C7DBlzp, Content-Type: application/json"
      
      ```

   6. Vào Profile-->connect như bài hướng dẫn trên, copy đoạn scipt đã chỉnh sửa xuống cuối script ip wan cũ, bấm apply là xong, ngắt kết nối pppoe và kết nối lại pppoe, khi nào lên chữ R đợi khoảng 1-2s là trên CF cũng sẽ update xong, chúc các bạn thành công

