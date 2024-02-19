import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import Button from "../../components/Button";

const Consent = () => {
    const [agreement, setAgreement] = useState(false)
    const navigate = useNavigate()
    const verifyAgreement = () => {
        if (agreement) {
            console.log("condition agreed")
            navigate('/verify-otp')

        }

        console.log("condition not agreed")
    }
  return (
    <section className="h-full px-24 pb-48 pt-48 pt-16">
      <div className="mx-auto h-full bg-boxBg flex rounded-2xl flex-col shadow-lg relative pt-8 text-left px-10">
        <div className="h-[88%] overflow-auto rounded-2xl">
          <div className="bg-[#d9d9d9] px-8 py-4">
            {/* from zelthy website */}
            <div className="terms_of_service_content">
              <p className="content-title">Terms of Service</p> <br />
              <p>
                Please read these Terms carefully because they are a binding
                agreement between You and Healthlane Technologies Pvt Ltd.,
                (“Zelthy” or “We”).
              </p>
              <br />
              <p>
                These Terms govern your use of the websites that link to these
                Terms. In these Terms, the word “Sites” refers to each of these
                websites and the services offered on those Sites. You
                automatically agree to these Terms and to our Privacy Statement
                simply by using or logging into the Sites.
              </p>
              <br />
              <p>
                Please note that we offer many services. Your use of Zelthy
                products or services are provided by Healthlane pursuant to a
                separate manually or digitally-executed agreement. Those
                additional terms become part of your agreement with us, if you
                use the services or log into the Sites.
              </p>
              <br />
              <br />
              <p className="content-title">A. Your Accounts</p>
              <br />
              <p>
                You may be required to create an account and specify a password
                in order to use certain services or features on the Sites. To
                create an account, you must be at least 18 years old and you
                must provide truthful and accurate information about yourself.
                Don’t try to impersonate anyone else when you create your
                account. If your information changes at any time, please update
                your account to reflect those changes.
              </p>
              <br />
              <p>
                In some cases, an account may be assigned to you by an
                administrator, such as your employer or educational institution.
                If you are using or logging into an account assigned to you by
                an administrator, additional terms may apply to your use of the
                Sites. Moreover, your administrator may be able to access or
                disable your account without our involvement.
              </p>
              <br />
              <p>
                You may not share your account with anyone else. Please keep
                your password confidential, and try not to use it on other
                websites. If you believe that your account has been compromised
                at any time, please notify your system administrator.
              </p>
              <br />
              <br />
              <p className="content-title">B. Modifications and Termination</p>
              <br />
              <p>
                We reserve the right to modify our Sites at any time, with or
                without notice to you. For example, we may add or remove
                functionality or features, and we may suspend or stop a
                particular feature altogether. We also reserve the right to
                charge a fee for any of our features at any time. If you don’t
                like any changes, you can stop using our Sites at any time.
              </p>
              <br />
              <br />
              <p className="content-title">C. Content You Post</p>
              <br />
              <p>
                We may provide opportunities for you to post text, photographs,
                videos, or other content (collectively, “Content”) on the Sites.
                You can only post Content if you own all the rights to that
                Content, or if another rights holder has given you permission.
              </p>
              <br />
              <p>
                You do not transfer ownership of your Content simply by posting
                it. However, by posting Content, you grant us, our agents,
                licensees, and assigns an irrevocable, perpetual (non-exclusive)
                right and permission to reproduce, encode, store, copy,
                transmit, publish, post, broadcast, display, publicly perform,
                adapt, modify, create derivative works of, exhibit, and
                otherwise use your Content. Without those rights, we couldn’t
                offer our Services. Please note that this license continues even
                if you stop using our Sites.
              </p>
              <br />
              <p>
                You agree to indemnify, release, and hold us harmless from any
                all liability, claims, actions, loss, harm, damage, injury, cost
                or expense arising out of any Content you post.
              </p>
              <br />
              <p>
                Keep in mind that if you send us any information, ideas,
                suggestions, or other communications to us, those communications
                will not be confidential. Moreover, unless we tell you
                otherwise, we reserve the right to reproduce, use, disclose, and
                distribute such communications without any obligation to you.
              </p>
              <br />
              <br />
              <p className="content-title">D. Content Posted by Others</p>
              <br />
              <p>
                We are not responsible for, and do not endorse, Content posted
                by any other person. Accordingly, we may not be held liable,
                directly or indirectly, for any loss or damage caused to you in
                connection with any Content posted by another member.
              </p>
              <br />
              <br />
              <p className="content-title">E. Your Use of the Sites</p>
              <br />
              <p>
                Please do not use the Sites in a way that violates any laws,
                infringes on anyone’s rights, is offensive, or interferes with
                the Sites or any features on the Sites (including any
                technological measures we employ to enforce these Terms).
              </p>
              <br />
              <p>
                It should be common sense, so we won’t bore you with a list of
                things you shouldn’t do. But if we (in our sole discretion)
                determine that you have acted inappropriately, we reserve the
                right to take down Content, terminate your account, prohibit you
                from using the Sites, and take appropriate legal actions.
              </p>
              <br />
              <p>
                Using our Site does not give you ownership of any intellectual
                property rights to the content you access. You may not use
                content from our Sites unless you obtain permission from us or
                its owner, or unless you are otherwise permitted by law.
              </p>
              <br />
              <p>
                When you use a Site or send communications to us through a Site,
                you are communicating with us electronically. You consent to
                receive electronically any communications related to your use of
                a Site. We may communicate with you by email or by posting
                notices on the Site. You agree that all agreements, notices,
                disclosures and other communications that are provided to you
                electronically satisfy any legal requirement that such
                communications be in writing. All notices from us intended for
                receipt by you shall be deemed delivered and effective when sent
                to the email address you provide to us. Please note that by
                submitting Content, creating a user account or otherwise
                providing us with your email address, postal address or phone
                number, you are agreeing that we or our agents may contact you
                at that address or number in a manner consistent with our
                Privacy Statement.
              </p>
              <br />
              <br />
              <p className="content-title">F. Intellectual Property</p>
              <br />
              <p>
                If you believe any Content on the Services infringes your
                copyrights, you may request that remove the Content from the
                Services (or disable access to that Content) by writing to{" "}
                <a href="mailto:contact@zelthy.com" alt="#">
                  contact@zelthy.com
                </a>
              </p>
              <br />
              <br />
              <p className="content-title">G. Our Warranties and Disclaimers</p>
              <br />
              <p>
                We provide our Services using a commercially reasonable level of
                care and promise to do our best to make sure you enjoy the
                Services. But there are certain things that we don’t promise
                about our Services.
              </p>
              <br />
              <p>
                OTHER THAN AS EXPRESSLY SET OUT IN THESE TERMS OF SERVICE,
                NEITHER HEALTHLANE TECHNOLOGIES PCT LTD NOR ITS AGENTS OR
                SERVICE PROVIDERS (THE “SERVICES ENTITIES”) MAKE ANY SPECIFIC
                PROMISES ABOUT THE SITES. FOR EXAMPLE, WE DON’T MAKE ANY
                COMMITMENTS ABOUT THE CONTENT WITHIN THE SITES, THE SPECIFIC
                FUNCTION OF THE SITES, OR THEIR RELIABILITY, AVAILABILITY, OR
                ABILITY TO MEET YOUR NEEDS. WE PROVIDE THE SITES “AS IS”.
              </p>
              <br />
              <p>
                SOME JURISDICTIONS PROVIDE FOR CERTAIN WARRANTIES, LIKE THE
                IMPLIED WARRANTY OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
                PURPOSE, AND NON-INFRINGEMENT. TO THE EXTENT PERMITTED BY LAW,
                WE EXCLUDE ALL WARRANTIES.
              </p>
              <br />
              <br />
              <p className="content-title">H. Liability for our Services</p>
              <br />
              <p>
                EXCEPT WHERE PROHIBITED, THE SERVICES ENTITIES SHALL NOT BE
                LIABLE FOR ANY INDIRECT, SPECIAL, INCIDENTAL, CONSEQUENTIAL, OR
                EXEMPLARY DAMAGES ARISING FROM YOUR USE OF THE SITES OR ANY
                THIRD PARTY’S USE OF THE SITES. THESE EXCLUSIONS INCLUDE,
                WITHOUT LIMITATION, DAMAGES FOR LOST PROFITS, LOST DATA,
                COMPUTER FAILURE, OR THE VIOLATION OF YOUR RIGHTS BY ANY THIRD
                PARTY, EVEN IF THE SERVICES ENTITIES HAVE BEEN ADVISED OF THE
                POSSIBILITY THEREOF AND REGARDLESS OF THE LEGAL OR EQUITABLE
                THEORY UPON WHICH THE CLAIM IS BASED.
              </p>
              <br />
              <br />
              <p className="content-title">I. Additional Details</p>
              <br />
              <p>
                We may modify these Terms at any time so be sure to check back
                regularly. By continuing to use or log in to a Site after these
                Terms have changed, you indicate your agreement to the revised
                Terms. If you do not agree to the changes, you should stop using
                or logging in to the Sites.
              </p>
              <br />
              <p>
                The Sites may contain links to third-party websites. That
                doesn’t mean that we control or endorse those websites, or any
                goods or services sold on those websites. Similarly, the Sites
                may contain ads from third-parties. We do not control or endorse
                any products being advertised.
              </p>
              <br />
              <p>
                If you do not comply with these Terms, and we don’t take action
                right away, this doesn’t mean we’re OK with what you did, or we
                are giving up any rights that we may have (such as taking action
                in the future).
              </p>
              <br />
              <p>
                These Terms are governed by and construed in accordance with the
                laws of India, without regard to its conflict of laws rules. You
                expressly agree that the exclusive jurisdiction for any claim or
                dispute under these Terms and or your use of the Services
                resides in the courts located in Gurugram, Harayna, and you
                further expressly agree to submit to the personal jurisdiction
                of such courts for the purpose of litigating any such claim or
                action. If it turns out that a particular provision in these
                Terms is not enforceable, that will not affect any other
                provision.
              </p>
              <br />
              <p>
                Healthlane accepts and responds to any requests such as
                disclosure, correction, addition, or deletion and veto of use or
                provision of personal information (the “Disclosure Requests”)
                from the person who provided his/her personal information.
              </p>
              <br />
              <p>
                Contact for inquiries regarding Personal Information Handling:{" "}
                <a href="mailto:privacy@zelthy.com" alt="#">
                  privacy@zelthy.com
                </a>
              </p>
              <br />
              <p>These terms were last updated on June 19, 2021.</p>
            </div>
          </div>
        </div>

        <div className="sticky bottom-0 ">
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <input
                type="checkbox"
                id="consent-form"
                className="accent-primary w-4 h-4 border rounded mr-2 cursor-pointer"
                name="consent-form"
                onChange={setAgreement}
                value={agreement}
              />
              <label
                className="text-xs text-[#757575] ml-2"
                htmlFor="consent-form"
              >
                I agree to the Terms of Service and Privacy Policy.
              </label>
              
            </div>
            <Button label="Submit" onClick={verifyAgreement}/>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Consent;
