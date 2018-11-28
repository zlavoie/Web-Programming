var Cashbonus;
var TotalC;

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

function AcctInfo(acctnum, balance,TypeOfAccount,trans){
    this.acctnum=acctnum;
    this.Initialbalance=balance;
    this.TotalBalance=balance;
    this.TypeOfAccount=TypeOfAccount;
    this.Transaction = trans;
    //document.write(acctnum+" "+balance+" "+TypeOfAccount);
}

function BankAccount(TypeOfAccount, balance, acctnum){
    this.TypeOfAccount = TypeOfAccount;
    this.balance = balance;
    this.Acct = acctnum;
    
    this.deposit = function(value,account,TransactionInfo) {
      for (var i=0;i<TransactionInfo.length;i++){
          if(TransactionInfo[i].acctnum === account){
              this.balance = Number(TransactionInfo[i].TotalBalance) + Number(this.balance);
              document.getElementById("amt").value="";
              return Number(this.balance);
          }
      }
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

$(document).ready( function () {
    $('#Check').DataTable();
    $('#Save').DataTable();
    $('#Bonus').DataTable();
$("#txtDate").datepicker().datepicker("setDate", new Date());
    var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
      
        this.classList.toggle("active");

       
        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
            panel.style.display = "none";
        } else {
            panel.style.display = "block";
        }
    });
}
} );

var modal = document.getElementById('id01');
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}  

document.getElementById("TransBtn").addEventListener("click", function(){
    //We have clicked submit and want to process the user data
   var account=document.getElementById("acctNum").value;
   var type = document.getElementById("type").value;
   var trans = document.getElementById("trans").value;
   var amt = document.getElementById("amt").value;
   var TransactionInfo=[];
        CheckingAccount.prototype = new BankAccount();
        CheckingAccount.prototype.constructor=CheckingAccount; 
    if(type === "Checking"){
    //document.getElementById("BalanceC").value=c.balance; 
    //document.getElementById("acctNumC").value="Checking";
       // findID(account);
        //NEED TO BE ABLE TO CREATE NEW ACCOUNT TO HANDLE THIS
        var c = new CheckingAccount("Checking",200,account);
        var info = new AcctInfo(account, amt,type,trans);
        TransactionInfo.push(info);
        
        if(document.getElementById("trans").value==="Deposit"){   
         TotalC=c.balance;
            c.deposit(document.getElementById("amt").value,account,TransactionInfo);    
      //  document.getElementById("BalanceC").value=c.balance;
      // FinalChecking=c.balance;
      //  document.getElementById("DepositC").value="";
    }
    }

//Withdrawal for checking account  
    /*
document.getElementById("WithdrawalBtnC").addEventListener("click", function(){
  var v=document.getElementById("WithdrawalC").value;
  ToStatement("Checking",v,"Withdrawal",Account);
  c.withdraw(v);
  document.getElementById("BalanceC").value=c.balance;
    FinalChecking=c.balance;
 document.getElementById("WithdrawalC").value="";}); */
/*
  document.getElementById("DepositBtnC").addEventListener("click", function(){
  var v=document.getElementById("DepositC").value;
  ToStatement("Checking",v,"Deposit",Account);
  c.deposit(v);
  document.getElementById("BalanceC").value=c.balance;
  FinalChecking=c.balance;
  document.getElementById("DepositC").value="";
  */
  });
/*

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
});*/