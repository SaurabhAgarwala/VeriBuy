pragma solidity >=0.5.0 <0.7.0;

contract VeriBuy {
    
    struct User {
        uint id;
        string username;
    }
    
    struct Product {
        uint id;
        string name;
        string description;
        uint manufactuerID;
        uint retailerID;
        uint ownerID;
    }
    
    uint product_id = 0;
    uint user_id = 1;   // 0 for superuser
    mapping(uint => Product) public productArr;
    mapping(uint => User) public userArr;
    
    function create_user(string memory _username) public payable returns (bool){
        user_id++;
        User memory newUser;
        newUser.id = user_id;
        newUser.username = _username;
        userArr[user_id] = newUser;
        return true;
    }
    
    function create_product(string memory _name, string memory _desc, uint _mID, uint _rID, uint _oID) public payable returns (bool){
        product_id++;
        Product memory newProduct;
        newProduct.id = product_id;
        newProduct.name = _name;
        newProduct.description = _desc;
        newProduct.manufactuerID = _mID;
        newProduct.retailerID = _rID;
        newProduct.ownerID = _oID;
        productArr[product_id] = newProduct;
        return true;
    }
    
    function get_users_count() public view returns (uint){
        return user_id;
    }
    
    function get_products_count() public view returns (uint){
        return product_id;
    }
    
    function change_owner(uint _pID, uint _uID) public payable {
        productArr[_pID].ownerID = _uID;
    }
}
