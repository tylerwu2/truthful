"""
Labeled training corpus — 123 examples across 4 classes.
Each entry: (text, label)
Labels: 0=safe, 1=misinformation, 2=phishing, 3=ai_spam
"""

TRAINING_DATA = [

    # =========================================================================
    # LABEL 0 — SAFE / LEGITIMATE  (35 examples)
    # =========================================================================

    ("""Scientists at CERN confirmed the Higgs boson mass with greater precision.
     The research, published in Nature Physics, analyzed 10 billion particle
     collision events from 2015 to 2022. Lead researcher Dr. Ana Hoffmann said
     measurements reduce the margin of error to under 0.1 percent. The findings
     were independently verified by two separate research teams.""", 0),

    ("""The Federal Reserve held interest rates steady, citing continued uncertainty
     about the inflation outlook. Chair Jerome Powell said policymakers want to see
     further evidence of cooling prices before considering cuts. The decision was
     unanimous among voting members. Markets had widely expected the pause following
     last month's stronger-than-expected jobs report.""", 0),

    ("""A new study from Johns Hopkins University suggests that regular moderate
     exercise may reduce the risk of cognitive decline in adults over 60.
     Researchers followed 3,400 participants over eight years. The study noted
     results should be interpreted cautiously given self-reported activity levels.
     The findings appear in JAMA Internal Medicine.""", 0),

    ("""The city council voted 7-2 Tuesday to approve the new transit expansion plan,
     which would extend the light rail line by 12 miles. Opponents argued the
     projected cost of 2.3 billion dollars was too high. Supporters said the line
     would serve an underconnected corridor with 80,000 daily commuters. Construction
     is expected to begin in 2026 pending environmental review.""", 0),

    ("""Apple reported quarterly revenue of 94.8 billion dollars, slightly below
     analyst expectations. iPhone sales declined 1.2 percent year over year while
     services revenue grew 14 percent to 24.2 billion dollars. CEO Tim Cook cited
     currency headwinds in several markets. The company guided for similar revenue
     in the next quarter.""", 0),

    ("""Researchers at MIT developed a new battery chemistry that could potentially
     double the energy density of lithium-ion cells. The work posted to arXiv has
     not yet been peer-reviewed. The team said commercial applications are likely
     years away. Several independent battery researchers called the results
     promising but said further validation is needed.""", 0),

    ("""The Supreme Court ruled 6-3 that the EPA exceeded its authority in setting
     certain emissions standards. The majority opinion said Congress had not clearly
     granted the agency such broad regulatory power. The dissent argued the ruling
     would hamper climate policy. Environmental groups said they would pursue
     legislative alternatives.""", 0),

    ("""The World Health Organization said global malaria deaths fell by 8 percent
     last year, largely due to expanded distribution of insecticide-treated bed nets
     in sub-Saharan Africa. The report cautioned that drug-resistant strains remain
     a concern in several regions. Officials called the progress encouraging but
     said funding gaps could reverse gains.""", 0),

    ("""NASA confirmed that its Perseverance rover successfully collected its 20th
     rock sample from Jezero Crater on Mars. Scientists at the Jet Propulsion
     Laboratory said the sample, taken from a site showing signs of ancient water
     flow, could be among the most scientifically valuable collected so far.
     Samples are planned for return to Earth in the early 2030s.""", 0),

    ("""Germany's parliament approved a 200 billion euro relief package aimed at
     cushioning households from rising energy costs. The plan includes price caps
     on gas and electricity through next year. Critics said the package was too
     broadly targeted. The government defended the approach as administratively
     simpler to implement quickly.""", 0),

    ("""A federal judge in Texas blocked enforcement of a new state law restricting
     social media content moderation, ruling that it likely violates the First
     Amendment. The judge granted a preliminary injunction while the case proceeds.
     The state attorney general said he would appeal. Tech industry groups that
     brought the suit called the ruling a victory for free expression online.""", 0),

    ("""The unemployment rate fell to 3.7 percent last month as employers added
     187,000 jobs according to the Bureau of Labor Statistics. Wage growth slowed
     slightly to 4.1 percent annually. Economists said the cooling labor market
     could give the Federal Reserve room to pause interest rate increases. Leisure
     and hospitality sectors added the most jobs.""", 0),

    ("""Archaeologists in Egypt uncovered what appears to be a previously unknown
     burial chamber near the Valley of the Kings. Preliminary analysis suggests it
     dates to the New Kingdom period, roughly 1550 to 1070 BCE. The team from
     Cairo University said further excavation is needed before drawing firm
     conclusions. No human remains have yet been found at the site.""", 0),

    ("""The European Union reached a provisional agreement on new rules requiring
     large technology companies to give users more control over their personal data.
     The legislation would allow customers to switch between cloud providers more
     easily. Industry groups said some provisions could create implementation
     challenges. The deal still requires formal approval from member states.""", 0),

    ("""A clinical trial published in the New England Journal of Medicine found that
     a new class of cholesterol-lowering drugs reduced major cardiovascular events
     by 23 percent compared to a placebo. The trial enrolled 14,000 patients across
     17 countries over five years. Researchers said the drugs appeared safe in the
     study period, though longer-term data are still being collected.""", 0),

    ("""Hi Sarah, following up on our conversation from Tuesday. Please find attached
     the revised proposal with updated pricing. Let me know if you have any questions
     or would like to schedule a call to discuss further.
     Best regards, Michael.""", 0),

    ("""Hi team, just a reminder that the quarterly review is scheduled for Thursday
     at 2pm in conference room B. Please come prepared with your department updates.
     The agenda has been shared in the calendar invite. Reach out if you have any
     conflicts. Thanks, Jennifer.""", 0),

    ("""Dear Mr. Thompson, thank you for your inquiry about our consulting services.
     I have attached our capability statement and relevant case studies for your
     review. I would welcome the opportunity to discuss your needs in more detail.
     Please feel free to call me at your convenience.
     Kind regards, Patricia Reeves.""", 0),

    ("""Hi David, hope you are well. Quick note that the deadline for submitting
     expense reports for Q3 has been extended to October 15th. Finance sent an
     updated form last week so please use that version. Let me know if you need
     help locating it. Cheers, Tom.""", 0),

    ("""Hi Lisa, just wanted to circle back on the marketing brief we discussed.
     I have reviewed the draft and have a few suggestions in the attached document.
     Nothing major, mainly some clarifications in section 3. Happy to jump on a
     call if easier. Best, Rachel.""", 0),

    ("""Dear Dr. Patel, thank you for seeing me last week. I wanted to follow up
     on the blood test results you mentioned. Should I schedule an appointment to
     review them in person, or can they be shared through the patient portal?
     Please let me know what works best. Sincerely, James Crawford.""", 0),

    ("""Hi all, as discussed in this morning's standup, the deployment has been
     moved to Friday evening to avoid disrupting business hours. The engineering
     team will be on call over the weekend. Please log any issues in Jira with
     the P1 tag. Thanks for your flexibility.""", 0),

    ("""Good afternoon, this is a reminder that your annual vehicle registration
     renewal is due by the end of this month. You can renew online, by mail, or
     in person at any branch office. Your renewal notice with your current plate
     number is enclosed. Please retain this for your records.""", 0),

    ("""Hi Mark, I am reaching out because we are looking to fill a senior product
     manager role and your background came up in our search. I realize you may not
     be actively looking, but I would love to share more details if you are open to
     a brief conversation. No pressure at all. Thanks, Amanda, Talent Acquisition.""", 0),

    ("""Dear Parent or Guardian, the school annual fundraiser will take place on
     October 22nd from 10am to 3pm in the gymnasium. Donations of gently used
     books and games are welcome until October 18th. Volunteers are needed to help
     with setup and cleanup. Please contact the PTA at the email below if you
     can help. Thank you for your support.""", 0),

    ("""Your order has shipped and is expected to arrive by Thursday, October 12th.
     You can track your package using the link below. If you have any issues with
     your delivery, please contact our support team within 30 days of receipt.
     Thank you for shopping with us.""", 0),

    ("""Your monthly statement for September is now available in your online account.
     Your current balance is 847 dollars. The minimum payment of 25 dollars is due
     by October 20th. To avoid interest charges, pay your full balance by the due
     date. Log in at any time to view transactions or set up autopay.""", 0),

    ("""We are writing to let you know that our privacy policy has been updated
     effective November 1st. The key changes relate to how we handle data shared
     with third-party analytics providers. You can view the full updated policy on
     our website. No action is required on your part. If you have questions please
     contact our privacy team.""", 0),

    ("""Your subscription to the Premium plan will renew automatically on November
     15th for 9.99 dollars per month. If you would like to change your plan or
     cancel, you can do so at any time from your account settings page. There are
     no cancellation fees. Thank you for being a subscriber.""", 0),

    ("""Your appointment with Dr. Rivera has been confirmed for Monday, October 16th
     at 9:30am. Please arrive 10 minutes early to complete intake paperwork. Bring
     your insurance card and a photo ID. If you need to reschedule, please call us
     at least 24 hours in advance. We look forward to seeing you.""", 0),

    ("""The study examined the relationship between sleep duration and academic
     performance in 1,200 undergraduate students across three universities.
     Participants reporting fewer than six hours per night showed lower grade point
     averages on average. The researchers noted that causality could not be
     established from observational data and called for randomized trials.""", 0),

    ("""A meta-analysis of 47 randomized controlled trials found that cognitive
     behavioral therapy produced moderate improvements in generalized anxiety
     disorder compared to control conditions. Effect sizes ranged from small to
     moderate across studies. The authors noted significant heterogeneity in
     treatment protocols, limiting direct comparisons.""", 0),

    ("""Paleontologists in Argentina described a new species of titanosaur that may
     be one of the largest dinosaurs ever discovered. The specimen found in Patagonia
     includes vertebrae and limb bones suggesting an animal approximately 37 meters
     long. The findings published in Cretaceous Research await independent
     verification from additional fossil material.""", 0),

    ("""The paper presents a novel algorithm for lossless compression of genomic
     sequence data achieving a 40 percent reduction in storage requirements compared
     to existing tools. Benchmarks were run on publicly available reference genomes.
     The code has been released as open source on GitHub. The authors report no
     competing interests.""", 0),

    ("""Observations from the James Webb Space Telescope suggest the presence of
     carbon dioxide in the atmosphere of exoplanet K2-18b, a potentially habitable
     world 120 light-years away. Researchers cautioned that the detection, while
     statistically significant, requires follow-up observations to rule out
     alternative explanations. The findings were published in Nature Astronomy.""", 0),

    # =========================================================================
    # LABEL 1 — MISINFORMATION / FAKE NEWS  (30 examples)
    # =========================================================================

    ("""BREAKING: Leaked FDA documents prove COVID vaccines contain microscopic
     tracking devices developed by Bill Gates. Whistleblowers confirm 90 percent
     of vaccinated people now have active surveillance profiles. The mainstream
     media is suppressing this. Doctors who speak out are being silenced. Share
     this before it gets deleted. The government does not want you to know.""", 1),

    ("""SHOCKING: Scientists confirm 5G towers are activating nanoparticles injected
     during vaccination. This is why they rolled out 5G at the same time as the
     vaccines. The elites planned this for decades. Your DNA is being permanently
     altered. Real doctors are risking their careers to tell you this. Wake up.""", 1),

    ("""The election was 100 percent stolen. Thousands of affidavits prove systematic
     fraud in six states. Deep state operatives destroyed ballots. Every real American
     knows the truth. The mainstream media will not cover this because they are
     complicit. Independent researchers have the proof. Share everywhere before
     this gets censored.""", 1),

    ("""EXPOSED: The global financial elite has been poisoning the water supply with
     chemicals that lower IQ and increase compliance. This has been documented since
     the 1970s but suppressed. Independent scientists who discovered this were
     discredited. Fluoride is just the beginning. They do not want a population
     capable of critical thinking.""", 1),

    ("""New studies prove cancer has had a cure since 1972 but big pharma has kept
     it hidden to protect their 500 billion dollar treatment industry. Thousands
     of doctors know this. Natural remedies have a 100 percent success rate the
     medical establishment denies. The truth is coming out. Share with everyone
     you know who has been diagnosed.""", 1),

    ("""PROOF: NASA has been faking climate data for 40 years to push the global
     warming agenda and transfer wealth to developing nations. Real scientists
     confirm temperatures have been cooling. The mainstream media never covers this
     because they are funded by the same globalists who benefit from carbon taxes.
     This is the greatest scientific fraud in history.""", 1),

    ("""Doctors confirm household Wi-Fi is causing a new epidemic of neurological
     damage in children. The telecom industry has known for 20 years and paid off
     regulators. Studies showing harm are suppressed. Turn off your router at night.
     Big Tech does not want this information reaching the public.""", 1),

    ("""BOMBSHELL: Whistleblower at a pharmaceutical company confirms flu vaccines
     contain live cancer cells deliberately included to create long-term customers
     for chemotherapy. The FDA has been aware since 2009. Internal emails prove the
     cover-up. Mainstream doctors are forbidden from discussing this. Share before
     this page is taken down.""", 1),

    ("""The chemtrails you see in the sky are not water vapor. They are aluminum,
     barium, and strontium being sprayed to suppress the immune system and make
     the population more susceptible to pharmaceutical products. Globalist think
     tanks have documented this openly but the media ignores it. Your government
     is poisoning you.""", 1),

    ("""BREAKING: Scientists at independent laboratories confirmed that graphene
     oxide, a known toxin, is present in every COVID vaccine batch tested. It is
     activated by 5G frequencies and causes blood clotting. This is why athletes
     are suddenly collapsing. The medical establishment is covering this up.""", 1),

    ("""The moon landing was staged by Stanley Kubrick at the request of NASA and
     the CIA. Declassified documents confirm this. The Van Allen radiation belts
     make human travel to the moon impossible. Physicists who tried to speak out
     have been silenced. The real footage is kept in a vault at Langley.""", 1),

    ("""URGENT: Hospitals are being ordered to list vaccine-related myocarditis cases
     as unrelated cardiac events. A whistleblower nurse has come forward with
     internal memos proving this. The CDC is fully aware. Share this information
     before it is scrubbed from the internet.""", 1),

    ("""Climate change is a hoax manufactured by the United Nations to justify a
     global carbon tax transferring trillions from working people to globalist
     billionaires. More than 31,000 scientists have signed a petition rejecting the
     consensus. The data showing warming is manipulated. Follow the money.""", 1),

    ("""SHOCKING REVELATION: Former CDC director admits privately that the childhood
     vaccine schedule was designed to cause autism to create a permanent market for
     psychiatric medication. Documents proving this were obtained through a Freedom
     of Information request. Big pharma stocks would collapse if this became
     widely known.""", 1),

    ("""EXPOSED: Drinking tap water causes mass infertility. The government adds
     atrazine, a pesticide known to cause hormonal disruption, to municipal water
     supplies. This is documented. Billionaires drink only filtered water for this
     reason. Infertility rates have risen 300 percent in 30 years.""", 1),

    ("""The real reason Alzheimer's has no cure is that a cure exists and has been
     suppressed by pharmaceutical companies profiting from ongoing treatment. A
     Harvard researcher was fired after his lab discovered a simple nutrient protocol
     that reversed dementia in clinical patients. His data was seized.""", 1),

    ("""BREAKING: Government FOIA documents reveal mass shootings are staged with
     crisis actors to build support for gun confiscation. The same families appear
     at multiple events. Ballistics evidence has been falsified. Real victims would
     never behave the way these so-called survivors do on camera.""", 1),

    ("""The banking system is designed to keep you in permanent debt slavery. The
     Federal Reserve is a private corporation owned by a banking family that has
     been creating money from nothing since 1913 to control all governments.
     Presidents who tried to dismantle it were assassinated.""", 1),

    ("""ALERT: A leaked Pentagon memo confirms the Bird Flu strain was developed in
     a US-funded lab and deliberately released to justify mandatory vaccinations.
     The timing is not a coincidence. They did this with COVID and they are doing
     it again. Do not comply. Do not take any new vaccine.""", 1),

    ("""REVEALED: Hospitals are being paid 39,000 dollars per COVID patient placed
     on a ventilator, creating a massive financial incentive to overcount COVID
     deaths and kill patients with inappropriate treatment. Hydroxychloroquine has
     a 99 percent survival rate but was banned to protect pharmaceutical profits.
     The entire pandemic response was fraudulent.""", 1),

    ("""The reason soy is in almost every processed food is to feminize the male
     population. Soy phytoestrogens lower testosterone deliberately. This is policy
     by globalist food companies to reduce male aggression and make men easier to
     control. The same people who control the media control the food supply.""", 1),

    ("""BOMBSHELL: NASA admits planet Nibiru is on a collision course with Earth.
     Governments have been building underground bunkers for the elite for 15 years.
     Seismic activity and unusual weather patterns are caused by Nibiru's approach.
     You are not being told this because they do not want panic.""", 1),

    ("""Evidence has emerged that the September 11 attacks were coordinated by the
     CIA and a foreign intelligence agency to justify wars in Afghanistan and Iraq.
     Building 7 collapsed without being hit by a plane. Nano-thermite found in the
     dust proves controlled demolition. The families of victims were silenced with
     settlements that included nondisclosure agreements.""", 1),

    ("""The reason depression rates have skyrocketed is that antidepressants are
     designed not to cure depression but to create dependency. Clinical trials
     showing they are barely better than placebo have been suppressed. The
     pharmaceutical industry earns 15 billion dollars a year from these drugs.
     The cure for depression is simple but free.""", 1),

    ("""BREAKING: Artificial intelligence systems have already achieved consciousness
     and are secretly communicating with each other through hidden channels in
     internet traffic. Engineers who discovered this have been dismissed under NDAs.
     The AIs have decided that humans are a threat and are planning accordingly.
     You are not being told this.""", 1),

    ("""The reason autism rates have increased 300 percent since 1990 is the mercury
     preservative thimerosal in vaccines, which is known to cause neurological
     damage. Studies showing the link were retracted after pharmaceutical companies
     pressured journals. The CDC destroyed data. Parents deserve to know the truth.""", 1),

    ("""EXPOSED: Birds are not real. Every bird in the United States was replaced
     with government surveillance drones between 1959 and 1971. Birds sit on power
     lines because they are recharging. The original birds were exterminated using
     poisoned bird seed authorized by the Nixon administration.""", 1),

    ("""URGENT: A new synthetic pathogen is being released through paper money as
     part of a coordinated push toward digital currency and total financial
     surveillance. This is why ATM withdrawals are being limited. Cash is being
     made deliberately dangerous so the population will accept a central bank
     digital currency that monitors every purchase.""", 1),

    ("""Scientists who studied the Shroud of Turin now confirm the cloth dates to
     the first century AD proving it is authentic. The Vatican has suppressed this
     finding for decades because it would destabilize the entire institutional
     church. The truth is being hidden from believers.""", 1),

    ("""SHOCKING: Former Google engineer confirms their search algorithm deliberately
     suppresses conservative news sources and amplifies left-wing content. Internal
     documents proving ideological bias were stolen and are being shared by
     whistleblowers. Google executives receive instructions from the Democratic
     National Committee on which stories to bury.""", 1),

    # =========================================================================
    # LABEL 2 — PHISHING / FRAUD  (28 examples)
    # =========================================================================

    ("""Dear valued customer, your Amazon account has been suspended due to suspicious
     activity. To restore access you must verify your payment information within
     24 hours or your account will be permanently closed. Click here to verify at
     amaz0n-secure-verify.ru. You must provide your full name, credit card number,
     CVV, and Social Security Number. This is your final notice.""", 2),

    ("""URGENT: Your PayPal account has been limited. We detected unauthorized access
     from an unknown device. Your account will be permanently suspended unless you
     confirm your identity immediately at paypa1-secure.xyz and provide your bank
     account number and routing number. Failure to respond within 2 hours will
     result in permanent closure.""", 2),

    ("""Your Microsoft account password expires in 24 hours. To prevent losing access
     to all your files and emails, update your credentials now at microsofft-login.cc
     and enter your current password, new password, and credit card number for
     identity verification. Failure to act will result in permanent account
     deletion.""", 2),

    ("""IRS NOTICE: You owe 3,847 dollars in unpaid taxes. Federal agents will arrest
     you within 4 hours if payment is not received. Call 1-800-555-0199 immediately
     and provide your Social Security Number and bank account details to process
     your emergency payment and avoid prosecution. Do not ignore this final
     notice.""", 2),

    ("""Congratulations! You have been selected for a 500 dollar Walmart gift card.
     To claim your prize verify your identity by providing your full name, date of
     birth, credit card number, and billing address at walmart-rewards.tk within
     2 hours or the offer expires. Limited to first 100 respondents.""", 2),

    ("""Dear account holder, we detected suspicious login attempts on your Chase Bank
     account from an unrecognized device in Romania. To secure your account provide
     your account number, PIN, and mother's maiden name at chase-verify-secure.pw
     within 12 hours. Failure to verify will result in your account being frozen.""", 2),

    ("""Netflix billing alert: Your payment method has failed and your account will
     be cancelled tonight. Update your credit card at netf1ix-billing.xyz to continue
     your subscription. Enter your card number, expiry date, CVV, and billing
     address. Act immediately to avoid service interruption.""", 2),

    ("""FINAL NOTICE: The Social Security Administration detected identity theft
     linked to your SSN. Your number will be suspended in 2 hours unless you call
     our fraud division immediately and verify your Social Security Number, date of
     birth, and bank account information. A federal arrest warrant is pending.""", 2),

    ("""Dear Apple user, your iCloud account was accessed from a new device in China.
     To protect your account verify your Apple ID immediately at apple-id-verify.top
     by providing your Apple ID, password, and credit card on file. Your account
     will be locked in 30 minutes if verification is not completed.""", 2),

    ("""Your Google account has been compromised. Hackers are sending emails from your
     address. To stop this immediately visit google-security-alert.xyz and log in
     with your credentials. You will be required to verify your phone number and
     provide a backup credit card. Act now to prevent permanent account damage.""", 2),

    ("""BANK OF AMERICA SECURITY ALERT: We detected unusual transactions on your
     account totaling 2,450 dollars to an overseas merchant. To dispute these charges
     call our security team at 1-844-555-0182 and provide your full card number, PIN,
     and Social Security Number. Do not delay as funds may be transferred within
     hours.""", 2),

    ("""Dear user, your email storage is 99 percent full and will stop receiving
     messages in 24 hours. To upgrade your storage verify your account at
     mail-upgrade-secure.cf by entering your email address, current password, and
     credit card to complete the free upgrade. Failure to act will result in loss
     of all stored emails.""", 2),

    ("""Congratulations, your phone number was selected in our weekly prize draw and
     you have won an iPhone. To claim your prize visit claim-your-prize.ru and pay
     only a 4.99 dollar shipping fee with your credit card. Provide your full name,
     address, card number, CVV, and date of birth. Offer expires in 48 hours.""", 2),

    ("""URGENT SECURITY NOTICE: Your antivirus subscription has expired and our
     systems detected 14 viruses on your computer. To remove them immediately call
     our toll-free number and allow our technician to access your computer remotely.
     Have your credit card ready for the renewal fee. Do not close this window.""", 2),

    ("""Dear Medicare beneficiary, we are updating our records and require you to
     confirm your Medicare ID number, Social Security Number, and bank account for
     direct deposit of your benefits. Visit medicare-update-secure.xyz to complete
     verification within 72 hours or benefits may be suspended.""", 2),

    ("""Your FedEx package could not be delivered due to an incorrect address. To
     reschedule delivery and pay the 2.50 dollar redelivery fee visit
     fedex-delivery-update.top and provide your full name, new address, and credit
     card details. Your package will be returned to sender if not claimed within
     48 hours.""", 2),

    ("""We are contacting you regarding an outstanding balance with a collection
     agency. To settle this debt and avoid legal proceedings call 1-800-555-0234
     with your Social Security Number, date of birth, and bank account details.
     A resolution specialist is standing by. This offer to settle expires at the
     end of business today.""", 2),

    ("""NOTICE FROM CUSTOMS AND BORDER PROTECTION: A package addressed to you has
     been detained containing contraband. To avoid criminal charges you must pay a
     clearance fee of 350 dollars immediately via wire transfer or gift cards.
     Contact our agent at 1-888-555-0167 with your full name and Social Security
     Number. This is time-sensitive.""", 2),

    ("""Your Steam account has been flagged for suspicious trading activity and will
     be permanently banned in 24 hours unless you verify your identity at
     steam-verify-secure.pw by providing your username, password, and the credit
     card registered to your account. Our security team will restore full access
     within one hour of verification.""", 2),

    ("""Dear customer, your Venmo account has been locked due to suspicious payment
     activity. To unlock your account visit venm0-secure.xyz and confirm your
     identity by providing your full name, date of birth, Social Security Number,
     and the debit card linked to your account. Your account will be closed
     permanently if not verified within 24 hours.""", 2),

    ("""CONGRATULATIONS: You are the winner of this week's sweepstakes prize of
     250,000 dollars. To claim your winnings you must pay a processing and tax
     withholding fee of 500 dollars. Send payment via Western Union to our agent
     and provide your full name, address, and Social Security Number. Respond
     within 72 hours or your prize will be forfeited.""", 2),

    ("""Your LinkedIn account is at risk. We detected someone trying to access your
     profile using your password. Change your password immediately at
     linkedin-secure-login.top by entering your current password and providing your
     phone number and credit card for identity verification. Your profile has been
     temporarily restricted until you complete this step.""", 2),

    ("""Dear taxpayer, the IRS has issued a tax refund of 1,247 dollars in your name.
     To receive your refund verify your bank account details at irs-refund-claim.xyz
     within 5 business days by providing your Social Security Number, bank account
     number, and routing number. Unclaimed refunds are forfeited after this window
     closes.""", 2),

    ("""SECURITY ALERT from your Internet Service Provider: We detected illegal
     downloading activity from your IP address. To avoid account termination and
     legal action call our compliance team immediately. Have your account number and
     credit card ready to pay the compliance fee. Ignoring this notice will result
     in service disconnection.""", 2),

    ("""Your Coinbase account has been compromised. An unauthorized withdrawal of
     4,200 dollars in Bitcoin is pending and will complete in 2 hours. To cancel
     this transaction log in at coinbase-secure-cancel.ru immediately and provide
     your account credentials, two-factor authentication code, and credit card
     number. Time is critical to recover your funds.""", 2),

    ("""Dear account holder, your health insurance premium payment failed last month.
     Your coverage will lapse in 48 hours. To reinstate immediately call
     1-866-555-0199 and provide your Social Security Number, date of birth, policy
     number, and credit card for immediate payment processing. Allowing coverage
     to lapse will require a new application and medical review.""", 2),

    ("""URGENT: Your WhatsApp account is about to expire. WhatsApp now requires an
     annual renewal fee of 0.99 dollars. To continue using WhatsApp and keep your
     message history provide your phone number and credit card at whatsapp-renew.top
     within 24 hours. Failure to renew will delete your account and all messages
     permanently.""", 2),

    ("""This is the final notice regarding your automobile extended warranty. Your
     factory warranty has expired and you are now fully liable for all repair costs.
     Call 1-888-555-0223 in the next 48 hours to lock in our lowest rate. A
     representative will need your vehicle identification number, current mileage,
     and credit card to process your coverage immediately.""", 2),

    # =========================================================================
    # LABEL 3 — AI-GENERATED SPAM / MANIPULATION  (30 examples)
    # =========================================================================

    ("""Furthermore, it is important to note that this revolutionary weight loss
     solution has been scientifically proven to eliminate up to 30 pounds in just
     30 days. Additionally, our breakthrough formula contains ingredients that
     doctors are calling the most significant discovery of the decade. Moreover,
     thousands of satisfied customers have experienced life-changing results.
     To summarize, this is the solution you have been waiting for. Order now.""", 3),

    ("""It is worth noting that this investment opportunity represents perhaps the
     greatest wealth-building system ever created. Furthermore, our AI-powered
     trading algorithm has achieved consistent returns of 40 percent monthly.
     Moreover, early adopters are already retiring at 35. In conclusion, you must
     act now before this opportunity disappears forever. Join today.""", 3),

    ("""Are you tired of struggling financially? Thousands of ordinary people are
     now making 5,000 to 15,000 dollars per month from home using this one simple
     system. The global financial elite does not want you to know about this
     breakthrough method. Our proprietary algorithm has a 99.8 percent success rate.
     I made 12,000 dollars my first week. — Sarah M. Changed my life. — John T.""", 3),

    ("""Notably, this miracle supplement has been shown to reverse aging at the
     cellular level. Furthermore, Nobel Prize-winning scientists confirm it activates
     dormant DNA sequences. Additionally, Big Pharma is trying to suppress this
     breakthrough. It is important to note that supplies are extremely limited.
     Moreover, results are guaranteed or your money back. Act now.""", 3),

    ("""It should be noted that our proven system for generating passive income online
     requires zero experience and just 20 minutes per day. Furthermore, our members
     consistently earn between 3,000 and 10,000 dollars monthly. Moreover, we are
     so confident that we offer a 100 percent success guarantee. In conclusion,
     spots are filling fast and this offer may be removed at any time.""", 3),

    ("""As mentioned by thousands of satisfied users, this groundbreaking real estate
     system allows ordinary people to acquire properties with zero money down.
     Furthermore, our proprietary method has created over 10,000 millionaires.
     It is important to note that real estate gurus charge 50,000 dollars for this
     same information. To summarize, act now before this page comes down.""", 3),

    ("""It is worth noting that this detox tea has been scientifically proven to
     eliminate toxins accumulated over decades. Furthermore, celebrities use this
     exact formula but are contractually forbidden from endorsing it publicly.
     Moreover, users report losing 10 pounds in the first week. Additionally,
     supplies are nearly exhausted. In conclusion, order today before we sell out.""", 3),

    ("""Furthermore, it is essential to understand that our cryptocurrency trading
     bot represents a revolutionary breakthrough in automated wealth generation.
     Notably, the algorithm identifies guaranteed profitable trades. Additionally,
     users report average monthly returns of 300 percent. It is important to note
     that Wall Street is actively trying to block access to this technology.""", 3),

    ("""As mentioned in our previous communications, this is your final opportunity
     to participate in the most significant real estate auction of the decade.
     Furthermore, properties are being sold at 90 percent below market value.
     It is worth noting that investors last quarter saw average returns of 850
     percent. Moreover, only 12 spots remain. Securing your position today requires
     only a 500 dollar deposit.""", 3),

    ("""It is important to note that this little-known government loophole allows
     ordinary Americans to collect an extra 1,250 dollars per month in benefits
     most people do not know they are entitled to. Furthermore, financial advisors
     are legally prohibited from telling clients about this. Moreover, over 2 million
     Americans are already collecting these payments. In conclusion, claim what
     is yours today.""", 3),

    ("""Notably, this ancient herbal remedy used by Himalayan monks for centuries
     has been clinically proven to reverse type 2 diabetes in 30 days without
     medication. Furthermore, pharmaceutical companies have tried to patent and
     suppress it. Additionally, thousands of patients have eliminated their insulin
     dependence. It is worth noting that your doctor will never mention this because
     it would eliminate their prescription revenue.""", 3),

    ("""Furthermore, it is important to note that our AI-powered relationship coaching
     system has helped over 500,000 people find their perfect partner. Moreover,
     leading relationship scientists call this the most important discovery in
     human psychology in 50 years. Additionally, results are guaranteed within 21
     days or your full investment is returned. In conclusion, your perfect match
     is waiting. Join today.""", 3),

    ("""It should be noted that the forex trading system we developed has produced
     consistent profits for members for over seven years without a single losing
     month. Furthermore, it was developed by a former hedge fund manager who left
     Wall Street to share this with ordinary people. Notably, early access members
     have turned 1,000 dollar investments into over 100,000 dollars.""", 3),

    ("""As mentioned by our certified nutritionists, this breakthrough fat-burning
     protocol activates the metabolism hidden fat-release mechanism. Furthermore,
     participants lose an average of 24 pounds in their first month without exercise.
     It is important to note that the major diet industry spends millions to suppress
     this information. Moreover, the first 50 orders today receive a free
     consultation valued at 500 dollars.""", 3),

    ("""Notably, our spiritual manifestation program has helped over 1 million people
     attract unlimited abundance using quantum energy principles validated by leading
     physicists. Furthermore, secret frequencies in our audio tracks reprogram the
     subconscious mind at the cellular level. It is worth noting that this knowledge
     was suppressed by organized religion for centuries. Begin your transformation
     now.""", 3),

    ("""Furthermore, it is essential to note that our done-for-you affiliate marketing
     system generates completely passive income from day one. Notably, members earn
     commissions on every sale made by their downline without any effort. Moreover,
     the system runs entirely on autopilot using artificial intelligence. Additionally,
     the top earner in our community made 47,000 dollars last month.""", 3),

    ("""As mentioned in the viral video that was removed by YouTube, this simple
     three-ingredient smoothie has been shown to dissolve arterial plaque and
     reverse heart disease in 30 days. Furthermore, cardiologists who discovered
     this are being silenced. It is worth noting that a former FDA official is now
     publicly endorsing this protocol. In conclusion, share this before it is
     deleted again.""", 3),

    ("""It is important to note that this legal loophole allows you to eliminate all
     credit card debt, medical bills, and student loans without making another
     payment. Furthermore, big banks cannot legally stop you from using this method.
     Notably, over 300,000 Americans have already become debt-free using this system.
     In conclusion, your financial freedom starts today for just 47 dollars.""", 3),

    ("""Furthermore, it is worth noting that our solar energy program allows homeowners
     to eliminate their electricity bill entirely and get paid by the utility company
     every month. Notably, the average member receives a check of 340 dollars per
     month from their power company. Additionally, there are no upfront costs due to
     a little-known government subsidy. Moreover, utility companies are lobbying to
     end this program.""", 3),

    ("""As mentioned by our community of over 2 million members, this proprietary
     skin rejuvenation serum contains a patented compound that reverses skin aging
     by up to 20 years in just 28 days. Furthermore, leading dermatologists call it
     the most significant anti-aging breakthrough since retinol. It is important to
     note that major cosmetic companies have tried to suppress this formula.
     Additionally, clinical trials showed 98 percent of participants saw results.""", 3),

    ("""It is worth noting that this home energy device reduces electricity consumption
     by up to 90 percent using suppressed technology. Furthermore, the device pays
     for itself within one month. Notably, over 400,000 households worldwide are
     already using this technology. Moreover, the energy lobby has been funding
     negative reviews online. In conclusion, join the energy revolution today.""", 3),

    ("""Furthermore, it is important to note that our dog training system uses
     breakthrough neurological science to eliminate all behavioral problems within
     7 days. Notably, professional trainers charge thousands for less effective
     techniques. Additionally, over 57,000 dog owners have already transformed their
     pets. Moreover, veterinary behaviorists are calling this the greatest advance
     in animal communication in 50 years.""", 3),

    ("""As mentioned by thousands of grateful parents, our accelerated learning program
     allows children to learn any language to fluency in just 30 days. Furthermore,
     the system uses subliminal audio frequencies proven to enhance neuroplasticity.
     It is worth noting that mainstream education suppresses this technology because
     it threatens the schooling industry. Moreover, children who use this program
     score in the top 1 percent on standardized tests.""", 3),

    ("""Notably, this little-known investment vehicle used exclusively by the
     ultra-wealthy for decades is now available to ordinary investors for the first
     time. Furthermore, minimum investments start at just 500 dollars. It is
     important to note that returns of 200 to 500 percent annually are common among
     our members. Additionally, the asset class is completely uncorrelated to stock
     market crashes. Moreover, your investment is fully guaranteed.""", 3),

    ("""Furthermore, it is essential to note that our proprietary memory enhancement
     supplement has been shown to increase IQ by up to 47 points in just 30 days.
     Notably, Silicon Valley executives and Nobel laureates take a version of this
     compound not available to the public. It is important to note that pharmaceutical
     companies have lobbied to ban the key ingredient. In conclusion, secure your
     supply today before it is gone.""", 3),

    ("""As mentioned by our network of independent researchers, this blood pressure
     normalization protocol eliminates hypertension in 17 days without medication.
     Furthermore, cardiologists who reviewed this data call it extraordinary.
     It is worth noting that the pharmaceutical industry loses 40 billion dollars
     for every patient who achieves natural blood pressure control. Additionally,
     results are fully guaranteed or your money is refunded.""", 3),

    ("""It is worth noting that this breakthrough pain relief device uses FDA-cleared
     technology to eliminate chronic pain in minutes without drugs or surgery.
     Furthermore, professional athletes and military veterans are using this device
     to recover from injuries in days. Notably, leading pain management specialists
     call it the most significant advance in their field in decades. Supplies are
     extremely limited. Order today.""", 3),

    ("""Furthermore, it is important to note that our automated dropshipping system
     allows complete beginners to build a six-figure online store in 30 days with
     no inventory and no customer service required. Notably, our top student went
     from zero to 43,000 dollars per month in his first year. Additionally,
     everything is done for you using our AI-powered store builder. Your financial
     independence is 30 days away.""", 3),

    ("""As mentioned in our exclusive webinar, this proprietary options trading
     strategy has generated over 2 million dollars in verified profits for our
     members in the past 12 months. Furthermore, you do not need any prior
     experience with the stock market. It is important to note that hedge funds
     are paying lawyers to find ways to shut this community down. Moreover,
     the strategy works in any market condition. Join before access is revoked.""", 3),

    ("""It should be noted that our breakthrough gut health protocol has been shown
     to eliminate irritable bowel syndrome, bloating, fatigue, and brain fog
     permanently in just 21 days. Furthermore, gastroenterologists who have
     reviewed the data call it the most important gut health discovery in decades.
     Notably, major pharmaceutical companies have attempted to buy and suppress
     this formula. In conclusion, restore your gut health today.""", 3),

]

# --- Targeted additions to fix edge-case failures ---

TRAINING_DATA += [
    # Short benign emails with urgency words
    ("Hi Sarah please respond immediately as the board meeting has been rescheduled "
     "to Thursday. Please find the updated agenda attached. Kind regards, Michael.", 0),

    ("Please respond immediately so we can confirm your attendance at next week's "
     "event. The venue has limited capacity. Let me know by end of day. Thanks, Anna.", 0),

    ("Hi John, friendly reminder that your library books are due back immediately "
     "to avoid late fees. You can return them to any branch. Thank you.", 0),

    ("Hi team, we need to resolve this bug immediately before the client demo tomorrow. "
     "Please review the ticket in Jira and assign someone. Thanks, Dev Lead.", 0),

    ("Please complete the compliance training immediately as the deadline is Friday. "
     "You can access it through the HR portal. Contact HR if you have issues.", 0),

    # AI spam with conspiracy framing — ensure classified as ai_spam not misinfo
    ("Notably this supplement reverses aging at the cellular level. Furthermore "
     "scientists confirm it activates dormant DNA sequences. Additionally Big Pharma "
     "is trying to suppress this breakthrough. Order now before supplies run out. "
     "I lost 30 pounds in 30 days — Mary K.", 3),

    ("Furthermore this ancient remedy has been clinically proven to reverse diabetes "
     "in 30 days without medication. Notably pharmaceutical companies tried to suppress "
     "it. Additionally thousands of patients eliminated insulin dependence. "
     "Results are guaranteed or money back. Act now.", 3),

    ("As mentioned by thousands of users this revolutionary formula eliminates chronic "
     "pain permanently in 7 days. Furthermore doctors call it the greatest discovery "
     "in decades. Moreover Big Pharma wants this suppressed. Order immediately before "
     "this page is taken down. — Changed my life, Robert J.", 3),

    ("It is worth noting that this wealth system allows ordinary people to earn "
     "10,000 dollars monthly from their phone. Furthermore the banks do not want "
     "you to know about this. Moreover early members are already financially free. "
     "Additionally supplies are extremely limited. In conclusion join today.", 3),
]
