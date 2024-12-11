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


