var FinalChecking; //final values for checking/saving/bonus
var FinalSaving;
var FinalBonus; 
var Cashbonus;
var InitialCheck; //initial values of checking/saving/bonus
var InitialSave;
var InitialBonus;
var bonus=[];
var checking=[];
var savings=[];

//csb=checking/savings/bonus
   function ToStatement(csb,v,type,bnkacct) {
       if (csb==="Checking"){
           checking.push("Account Number: "+bnkacct+" |Account Type:"+String(csb)+" Transaction: "+String(type)+" Amount: $"+String(v));
       }else if(csb==="Savings"){
           savings.push("Account Number: "+bnkacct+" |Account Type:"+String(csb)+" Transaction: "+String(type)+" Amount: $"+String(v));
       }
       else{
           bonus.push("Account Number: "+bnkacct+" |Account Type:"+String(csb)+" Transaction: "+String(type)+" Amount: $"+String(v));
       }
    };

    function PrintStatement() {
    var Head1 = document.getElementById("Checktitle"); 
        var paragraph1 = document.getElementById("InitialCheck");
	var paragraph = document.getElementById("statementC");
        var myStatement="Checking Account";
        var myStatement1="Initial Amount: $"+InitialCheck;  
        Head1.innerHTML=myStatement;
        paragraph1.innerHTML=myStatement1;
        myStatement="";
        for(var i=0;i<checking.length;i++){
            myStatement=myStatement+"<li>"+String(checking[i])+"</li><br>";
        }
        myStatement=(myStatement+"<br> Final Balance For Checking Account: $"+FinalChecking);
        paragraph.innerHTML=myStatement;
        
        Head1 = document.getElementById("Savetitle"); 
        paragraph = document.getElementById("statementS");
        var paragraph1 = document.getElementById("InitialSave");
        myStatement="Savings Account";
        myStatement1="Initial Amount: $"+InitialSave;
        Head1.innerHTML=myStatement
        paragraph1.innerHTML=myStatement1;
        myStatement="";
        for(var a=0;a<savings.length;a++){
            myStatement=myStatement+"<li>"+String(savings[a])+"</li><br>";
        }
        myStatement=myStatement+"<br> Final Balance For Savings Account: $"+FinalSaving;
        paragraph.innerHTML=myStatement;
        
        Head1 = document.getElementById("Bonustitle"); 
        var s3 = "BonusAccount";
        Head1.innerHTML=s3;
        paragraph1 = document.getElementById("InitialBonus");
        s3="Initial Amount: $"+InitialBonus;
        paragraph1.innerHTML=s3;
        
        paragraph = document.getElementById("statementB");
        var m="";
        for(var k=0;k<bonus.length;k++){
            m=m+"<li>"+String(bonus[k])+"</li><br>";
        }
        m=m+"<br> Final Balance For Bonus Account: $"+FinalBonus;
        paragraph.innerHTML=m;
    };


function BankAccount(TypeOfAccount, balance, bnkacct){
    this.TypeOfAccount = TypeOfAccount;
    this.balance = balance;
    this.Acct = bnkacct;
    
    this.deposit = function(amount) {
	this.balance = this.balance + Number(amount);
    return Number(this.balance);
    };
    
    this.withdraw = function(amount) {
        var prev = this.balance;
		this.balance = this.balance - amount;
        if(this.balance < 0){
            alert("Insufficient Funds. Max Amount That Is Being Dispensed: $"+prev);
            return this.balance=0;
        }
        return Number(this.balance);
    };  
    
    this.GetBalance = function() {
        return this.balance;
    };   
}

// CheckingAccount
function CheckingAccount(TypeOfAccount, balance,bnkacct){
    //using BankAccount.call to inherit the Animal constructor (sort of like parent or super in other languages). 
    // ^ Found this online when i had trouble initialzing variables with constructor
    BankAccount.call(this, TypeOfAccount, balance,bnkacct);
    this.withdraw = function(amount) {   
        var over = Number(this.balance-amount);
	if(over < -500){
        alert("Insufficient Funds. Overdrafted.");
        
	}
	else{
        this.balance = this.balance - amount;
        //alert("Overdraft Protection Applied.");
	}};}

// SavingsAccount
function SavingsAccount(TypeOfAccount, balance){
    BankAccount.call(this, TypeOfAccount, balance);
    var interest = 0.3;
    
    this.Calc = function() {
	FinalSaving = (this.balance*interest) + this.balance;
	return FinalSaving;
    };
}

// BonusSavingsAccount
 function BonusAccount(TypeOfAccount, balance,bnkacct){
    SavingsAccount.call(this, TypeOfAccount, balance,bnkacct);
    
    this.withdraw = function(amount){	
	    this.balance = this.balance - (Number(amount)+10);
        if(Number(this.balance)<5000){
            Cashbonus=false;
        }
        else{
            Cashbonus=true;
        }
        return Number(this.balance);
    };
     
     this.Calc = function(){
       if(Cashbonus===true||Cashbonus===undefined)  {
        FinalBonus=this.balance+(this.balance*.3)+50;   
           return FinalBonus;
       }
         else{
             FinalBonus=this.balance+(this.balance*.3);
             return FinalBonus;
         }
     };
     
}

document.getElementById("AccountBtn").addEventListener("click", function(){
    Account=document.getElementById("Account").value;
    
InitialCheck=200;
CheckingAccount.prototype = new BankAccount();
CheckingAccount.prototype.constructor=CheckingAccount;  
var c = new CheckingAccount("Checking",InitialCheck,Account);
 document.getElementById("BalanceC").value=c.balance; 
 document.getElementById("acctNumC").value="Checking";
FinalChecking=c.balance;
    
//Withdrawal for checking account  
document.getElementById("WithdrawalBtnC").addEventListener("click", function(){
  var v=document.getElementById("WithdrawalC").value;
  ToStatement("Checking",v,"Withdrawal",Account);
  c.withdraw(v);
  document.getElementById("BalanceC").value=c.balance;
    FinalChecking=c.balance;
 document.getElementById("WithdrawalC").value="";});

//Deposit for checking account
  document.getElementById("DepositBtnC").addEventListener("click", function(){
  var v=document.getElementById("DepositC").value;
  ToStatement("Checking",v,"Deposit",Account);
  c.deposit(v);
  document.getElementById("BalanceC").value=c.balance;
  FinalChecking=c.balance;
  document.getElementById("DepositC").value="";});


//Set up initialization of account
InitialSave=200;
SavingsAccount.prototype = new BankAccount();
SavingsAccount.prototype.constructor=SavingsAccount;  
var s = new SavingsAccount("Savings",InitialSave,Account);
 document.getElementById("BalanceS").value=s.balance; 
 document.getElementById("acctNumS").value="Savings";
 FinalSaving=s.Calc(s.balance);
    
//Withdrawal for saving account  
document.getElementById("WithdrawalBtnS").addEventListener("click", function(){
  var v=document.getElementById("WithdrawalS").value;
  ToStatement("Savings",v,"Withdrawal",Account);
  s.withdraw(v);
  document.getElementById("BalanceS").value=s.balance;
    FinalSaving=s.Calc(s.balance);
 document.getElementById("WithdrawalS").value="";});
    
//Deposit for saving account
document.getElementById("DepositBtnS").addEventListener("click", function(){
  var v=document.getElementById("DepositS").value;
  ToStatement("Savings",v,"Deposit",Account);
    s.deposit(v);
  document.getElementById("BalanceS").value=s.balance;
    FinalSaving=s.Calc(s.balance);
  document.getElementById("DepositS").value="";});
    
  
InitialBonus = 5000;
BonusAccount.prototype = new SavingsAccount();
BonusAccount.prototype.constructor=BonusAccount;  
var b = new BonusAccount("Bonus",InitialBonus,Account);
document.getElementById("BalanceB").value=b.balance;  
 document.getElementById("acctNumB").value="Bonus";
FinalBonus=b.Calc();

//withdrawal for bonus account
document.getElementById("WithdrawalBtnB").addEventListener("click", function(){
  var v=document.getElementById("WithdrawalB").value;
  ToStatement("Bonus",v,"Withdrawal",Account);
  b.withdraw(v);
  document.getElementById("BalanceB").value=b.balance;
    FinalBonus=b.Calc();
 document.getElementById("WithdrawalB").value="";
});
    
//Deposit for bonus account
document.getElementById("DepositBtnB").addEventListener("click", function(){
  var v=document.getElementById("DepositB").value;
  ToStatement("Bonus",v,"Deposit",Account);
  b.deposit(v);
  FinalBonus=b.Calc();
  document.getElementById("BalanceB").value=b.balance;
  document.getElementById("DepositB").value="";
});


document.getElementById("StatementBtn").addEventListener("click", function(){
    d3.style.display="block";

PrintStatement(); 
});
});